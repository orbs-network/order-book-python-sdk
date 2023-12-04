from typing import TypedDict, List, Optional


class CreateOrderInput(TypedDict):
    price: str
    size: str
    symbol: str
    side: str
    clientOrderId: str


def gen_create_order_headers(*, signature: str, message_data: str):
    return {
        "X-API-SIGN": signature,
        "X-API-EIP712-MSG": message_data,
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
