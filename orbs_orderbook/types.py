from typing import Any, Dict, List, Optional, TypedDict
from dataclasses import dataclass, asdict
import json


def _snake_to_camel(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.capitalize() for x in components[1:])


def _camel_to_snake(camel_str: str) -> str:
    return "".join(["_" + i.lower() if i.isupper() else i for i in camel_str]).lstrip(
        "_"
    )


def _parse_to_class(cls, data: dict):
    snake_case_data = {_camel_to_snake(k): v for k, v in data.items()}
    return cls(**snake_case_data)


@dataclass
class Base:
    def to_camelcase_dict(self) -> dict:
        return {_snake_to_camel(k): v for k, v in asdict(self).items()}

    def to_json(self) -> str:
        return json.dumps(self.to_camelcase_dict())


@dataclass
class PaginationResponse:
    page: int
    page_size: int
    total: int
    total_pages: int


@dataclass
class CreateOrderInput(Base):
    price: str
    size: str
    symbol: str
    side: str
    client_order_id: str


@dataclass
class EIP712Message(Base):
    domain_separator: Dict[str, str]
    message_types: Dict[str, Any]
    message_data: Dict[str, Any]


@dataclass
class CreateOrderResponse(Base):
    order_id: str


@dataclass
class OrderResponse(Base):
    order_id: str
    client_order_id: Optional[str]
    user_id: Optional[str]
    price: str
    symbol: str
    size: str
    pending_size: str
    filled_size: str
    side: str
    timestamp: Optional[str]
    cancelled: bool


@dataclass
class CancelOrderResponse(Base):
    order_id: str


class SymbolResponse(TypedDict):
    symbol: str
    name: str


@dataclass
class MarketDepthData(Base):
    asks: List[List[str]]
    bids: List[List[str]]
    symbol: str
    time: int


@dataclass
class MarketDepthResponse(Base):
    code: str
    data: MarketDepthData


@dataclass
class OrdersForUserResponse(Base, PaginationResponse):
    data: List[OrderResponse]


@dataclass
class Token(Base):
    address: str
    decimals: int


@dataclass
class SupportedTokensResponse(Base):
    tokens: Dict[str, Token]
