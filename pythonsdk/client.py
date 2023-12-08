import json
from typing import Any, Dict, List, Optional

import requests

from pythonsdk.types import (
    CancelOrderResponse,
    CreateOrderInput,
    MarketDepthResponse,
    OrderResponse,
    OrdersForUserResponse,
    SymbolResponse,
    gen_create_order_headers,
)


class OrderBookSDK:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.headers = {
            "X-API-KEY": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

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
                method, url, headers=headers, data=json.dumps(data), timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            return {
                "error": err.response.reason,
                "status_code": err.response.status_code,
                "message": err.response.text,
            }

    def create_order(
        self, *, order_input: CreateOrderInput, signature: str, message_data: str
    ) -> OrderResponse:
        return self._send_request(
            method="POST",
            endpoint="api/v1/order",
            data={**order_input, "eip712Sig": signature, "eip712MsgData": message_data},
        )

    def cancel_order_by_id(self, order_id: str) -> CancelOrderResponse:
        return self._send_request(method="DELETE", endpoint=f"api/v1/order/{order_id}")

    def cancel_order_by_client_id(self, client_order_id: str) -> CancelOrderResponse:
        return self._send_request(
            method="DELETE", endpoint=f"api/v1/order/client-order/{client_order_id}"
        )

    def cancel_all_orders(self) -> Dict[str, Any]:
        return self._send_request(method="DELETE", endpoint="api/v1/orders")

    def get_symbols(self) -> List[SymbolResponse]:
        return self._send_request(method="GET", endpoint="api/v1/symbols")

    def get_order_by_id(self, order_id: str) -> OrderResponse:
        return self._send_request(method="GET", endpoint=f"api/v1/order/{order_id}")

    def get_order_by_client_id(self, client_order_id: str) -> OrderResponse:
        return self._send_request(
            method="GET", endpoint=f"api/v1/order/client-order/{client_order_id}"
        )

    def get_market_depth(self, symbol: str, limit: int) -> MarketDepthResponse:
        return self._send_request(
            method="GET", endpoint=f"api/v1/orderbook/{symbol}", data={"limit": limit}
        )

    def get_orders_for_user(self, page: int, page_size: int) -> OrdersForUserResponse:
        return self._send_request(
            method="GET",
            endpoint="api/v1/orders",
            data={"page": page, "pageSize": page_size},
        )
