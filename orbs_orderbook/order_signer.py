import random
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, Tuple

from eth_account import Account

from orbs_orderbook.client import OrderBookSDK
from orbs_orderbook.exceptions import (
    ErrDecimalPlaces,
    ErrInvalidSide,
    ErrInvalidSymbolFormat,
    ErrInvalidToken,
)
from orbs_orderbook.signer import Signer
from orbs_orderbook.types import CreateOrderInput, EIP712Message, Token
from orbs_orderbook.utils import convert_to_base_unit


class OrderSigner(Signer):
    __account: Account
    __sdk: OrderBookSDK

    def __init__(self, private_key: str, sdk: OrderBookSDK):
        super().__init__()

        self.__account = Account.from_key(private_key)
        self.__sdk = sdk

    def prepare_and_sign_order(
        self,
        order: CreateOrderInput,
        deadline: datetime = datetime.now() + timedelta(days=1),
    ) -> (str, dict):
        """Prepare EIP-712 message and sign it.

        Args:
            order: Order to sign.
            deadline (optional): How long the order signature is valid for.

        Returns:
            Tuple of signature and EIP712 message data (needed for signature validation)

        Raises:
            - ErrInvalidSymbolFormat: Raised when symbol does not follow "TOKEN1-TOKEN2" format
            - ErrInvalidSide: Raised when side is not "buy" or "sell"
            - ErrInvalidToken: Raised when token is not supported
        """
        in_token, out_token = self.__get_token_details(
            symbol=order.symbol, side=order.side
        )

        domain_data = self._construct_domain_data()
        message_types = self._construct_message_types()
        message_data = self._construct_message_data(
            in_token=in_token,
            out_token=out_token,
            size=order.size,
            price=order.price,
            side=order.side,
            signer_address=self.__account.address,
            deadline=deadline,
        )

        signable_message = self.encode_typed_data(
            primary_type="RePermitWitnessTransferFrom",
            domain_data=domain_data,
            message_types=message_types,
            message_data=message_data,
        )

        signature = self.sign_message(signable_message, self.__account.key)
        eip_712_msg = EIP712Message(
            domain_separator=domain_data,
            message_types=message_types,
            message_data=message_data,
        )

        return signature.signature.hex(), eip_712_msg

    def _construct_domain_data(self) -> Dict[str, str]:
        return {
            "name": "RePermit",
            "chainId": "137",
            "verifyingContract": "0x4d415B58EA43988FfF7f50A3475718b0858fE0f1",
        }

    def _construct_message_types(self) -> Dict[str, Any]:
        return {
            "RePermitWitnessTransferFrom": [
                {"name": "permitted", "type": "TokenPermissions"},
                {"name": "spender", "type": "address"},
                {"name": "nonce", "type": "uint256"},
                {"name": "deadline", "type": "uint256"},
                {"name": "witness", "type": "PartialOrder"},
            ],
            "TokenPermissions": [
                {"name": "token", "type": "address"},
                {"name": "amount", "type": "uint256"},
            ],
            "PartialOrder": [
                {"name": "info", "type": "OrderInfo"},
                {"name": "exclusiveFiller", "type": "address"},
                {"name": "exclusivityOverrideBps", "type": "uint256"},
                {"name": "input", "type": "PartialInput"},
                {"name": "outputs", "type": "PartialOutput[]"},
            ],
            "OrderInfo": [
                {"name": "reactor", "type": "address"},
                {"name": "swapper", "type": "address"},
                {"name": "nonce", "type": "uint256"},
                {"name": "deadline", "type": "uint256"},
                {"name": "additionalValidationContract", "type": "address"},
                {"name": "additionalValidationData", "type": "bytes"},
            ],
            "PartialInput": [
                {"name": "token", "type": "address"},
                {"name": "amount", "type": "uint256"},
            ],
            "PartialOutput": [
                {"name": "token", "type": "address"},
                {"name": "amount", "type": "uint256"},
                {"name": "recipient", "type": "address"},
            ],
        }

    def _construct_message_data(
        self,
        *,
        in_token: Token,
        out_token: Token,
        size: str,
        price: str,
        side: str,
        signer_address: str,
        deadline: datetime,
    ) -> Dict[str, Any]:
        price_dec = Decimal(price)
        size_dec = Decimal(size)

        self._check_decimal_places(price_dec)

        in_amount = self._calculate_in_amount(
            size=size_dec, price=price_dec, side=side, decimals=in_token.decimals
        )

        out_amount = self._calculate_out_amount(
            size=size_dec, price=price_dec, side=side, decimals=out_token.decimals
        )
        nonce = str(random.randint(0, 2**32 - 1))

        epoch_deadline = str(int(deadline.timestamp()))

        return {
            "permitted": {"token": in_token.address, "amount": str(in_amount)},
            "spender": "0x0B94c1A3E11F8aaA25D27cAf8DD05818e6f2Ad97",
            "nonce": nonce,
            "deadline": epoch_deadline,
            "witness": {
                "info": {
                    "reactor": "0x0B94c1A3E11F8aaA25D27cAf8DD05818e6f2Ad97",
                    "swapper": signer_address,
                    "nonce": nonce,
                    "deadline": epoch_deadline,
                    "additionalValidationContract": "0x0000000000000000000000000000000000000000",
                    "additionalValidationData": "0x",
                },
                "exclusiveFiller": "0x1a08D64Fb4a7D0b6DA5606A1e4619c147C3fB95e",
                "exclusivityOverrideBps": "0",
                "input": {"token": in_token.address, "amount": str(in_amount)},
                "outputs": [
                    {
                        "token": out_token.address,
                        "amount": str(out_amount),
                        "recipient": signer_address,
                    }
                ],
            },
        }

    def __get_token_details(self, *, symbol: str, side: str) -> Tuple[Token, Token]:
        if "-" not in symbol:
            raise ErrInvalidSymbolFormat(
                f"Invalid symbol format: {symbol}. Expected format 'TOKEN1-TOKEN2'."
            )

        if side not in ["buy", "sell"]:
            raise ErrInvalidSide(f"Invalid side: {side}. Expected 'buy' or 'sell'.")

        token_parts = symbol.upper().split("-")
        if len(token_parts) != 2:
            raise ErrInvalidSymbolFormat(
                f"Invalid symbol format: {symbol}. Expected format 'TOKEN1-TOKEN2'."
            )

        in_token_symbol, out_token_symbol = (
            token_parts if side == "sell" else token_parts[::-1]
        )

        in_token_dict = self.__sdk.supported_tokens.get(in_token_symbol)
        if not in_token_dict:
            raise ErrInvalidToken(f"Invalid 'in' token symbol: {in_token_symbol}.")

        out_token_dict = self.__sdk.supported_tokens.get(out_token_symbol)
        if not out_token_dict:
            raise ErrInvalidToken(f"Invalid 'out' token symbol: {out_token_symbol}.")

        return Token(**in_token_dict), Token(**out_token_dict)

    def _calculate_in_amount(
        self, *, size: Decimal, price: Decimal, side: str, decimals: int
    ) -> int:
        if side == "buy":
            return convert_to_base_unit(
                token_amount=size * price,
                decimals=decimals,
            )
        else:
            return convert_to_base_unit(
                token_amount=size,
                decimals=decimals,
            )

    def _calculate_out_amount(
        self, *, size: Decimal, price: Decimal, side: str, decimals: int
    ) -> int:
        if side == "sell":
            return convert_to_base_unit(
                token_amount=size * price,
                decimals=decimals,
            )
        else:
            return convert_to_base_unit(
                token_amount=size,
                decimals=decimals,
            )

    def _check_decimal_places(self, price: Decimal) -> None:
        decimal_tuple = price.as_tuple()
        decimal_places = max(0, -decimal_tuple.exponent)
        if decimal_places > 8:
            raise ErrDecimalPlaces(f"Price has more than 8 decimal places: {price}")
