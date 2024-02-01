import json
from typing import Any, Dict, List, Optional

import requests

import dataclasses

from orbs_orderbook.exceptions import ErrApiRequest, ErrUnauthorized
from orbs_orderbook.types import (
    CancelOrderResponse,
    CreateOrderInput,
    CreateOrderResponse,
    EIP712Message,
    MarketDepthResponse,
    OrderResponse,
    OrdersForUserResponse,
    _parse_to_class,
    SupportedTokensResponse,
    SymbolResponse,
)

from orbs_orderbook.utils import dataclass_serializer


class OrderBookSDK:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.headers = {
            "X-API-KEY": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.supported_tokens = self.get_supported_tokens().tokens

    def _send_request(
        self,
        *,
        method: str,
        endpoint: str,
        data: Optional[Any] = None,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        url = f"{self.base_url}/{endpoint}"
        headers = self.headers.copy()

        if custom_headers:
            headers.update(custom_headers)
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                data=json.dumps(data, default=dataclass_serializer),
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 401:
                raise ErrUnauthorized("Invalid API key") from err

            raise ErrApiRequest(
                status_code=err.response.status_code,
                message=err.response.json()["msg"],
            ) from err

    def create_order(
        self,
        *,
        order_input: CreateOrderInput,
        signature: str,
        message: EIP712Message,
    ) -> CreateOrderResponse:
        res = self._send_request(
            method="POST",
            endpoint="api/v1/order",
            data={
                **order_input.to_camelcase_dict(),
                "eip712Sig": signature,
                "eip712Msg": message.message_data,
            },
        )
        return _parse_to_class(CreateOrderResponse, res)

    def cancel_order_by_id(self, order_id: str) -> CancelOrderResponse:
        res = self._send_request(method="DELETE", endpoint=f"api/v1/order/{order_id}")
        return _parse_to_class(CancelOrderResponse, res)

    def cancel_order_by_client_id(self, client_order_id: str) -> CancelOrderResponse:
        res = self._send_request(
            method="DELETE", endpoint=f"api/v1/order/client-order/{client_order_id}"
        )
        return _parse_to_class(CancelOrderResponse, res)

    def cancel_all_orders(self) -> Dict[str, Any]:
        return self._send_request(method="DELETE", endpoint="api/v1/orders")

    def get_symbols(self) -> List[SymbolResponse]:
        return self._send_request(method="GET", endpoint="api/v1/symbols")

    def get_supported_tokens(self) -> SupportedTokensResponse:
        res = self._send_request(method="GET", endpoint="api/v1/supported-tokens")
        return _parse_to_class(SupportedTokensResponse, res)

    def get_order_by_id(self, order_id: str) -> OrderResponse:
        res = self._send_request(method="GET", endpoint=f"api/v1/order/{order_id}")
        return _parse_to_class(OrderResponse, res)

    def get_order_by_client_id(self, client_order_id: str) -> OrderResponse:
        res = self._send_request(
            method="GET", endpoint=f"api/v1/order/client-order/{client_order_id}"
        )
        return _parse_to_class(OrderResponse, res)

    def get_market_depth(self, symbol: str, limit: int) -> MarketDepthResponse:
        res = self._send_request(
            method="GET", endpoint=f"api/v1/orderbook/{symbol}", data={"limit": limit}
        )
        return _parse_to_class(MarketDepthResponse, res)

    def get_orders_for_user(self, page: int, page_size: int) -> OrdersForUserResponse:
        res = self._send_request(
            method="GET",
            endpoint="api/v1/orders",
            data={"page": page, "pageSize": page_size},
        )
        return _parse_to_class(OrdersForUserResponse, res)

    def get_filled_orders_for_user(
        self, page: int, page_size: int
    ) -> OrdersForUserResponse:
        res = self._send_request(
            method="GET",
            endpoint="api/v1/fills",
            data={"page": page, "pageSize": page_size},
        )
        return _parse_to_class(OrdersForUserResponse, res)
