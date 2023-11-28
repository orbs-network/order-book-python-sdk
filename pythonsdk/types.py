from typing import TypedDict, List, Optional, Dict, Any, TypeVar, Generic


class PlaceOrderInput(TypedDict):
    price: str
    size: str
    symbol: str
    side: str
    clientOrderId: str


def create_place_order_headers(*, signature: str, timestamp: str):
    return {
        "X-API-SIGN": signature,
        "X-API-TIMESTAMP": timestamp,
    }


class OrderResponse(TypedDict):
    orderId: str
    clientOrderId: Optional[str]
    userId: Optional[str]
    price: str
    symbol: str
    size: str
    side: str
    timestamp: Optional[str]


class CancelOrderResponse(TypedDict):
    orderId: str


class SymbolResponse(TypedDict):
    symbol: str


class MarketDepthData(TypedDict):
    asks: List[List[str]]
    bids: List[List[str]]
    symbol: str
    time: int


class MarketDepthResponse(TypedDict):
    code: str
    data: MarketDepthData


class OrdersForUserResponse(TypedDict):
    data: List[OrderResponse]
    page: int
    pageSize: int
    total: int
    totalPages: int
