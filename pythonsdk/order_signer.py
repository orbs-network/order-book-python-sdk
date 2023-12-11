import datetime
import json
import random
from importlib import resources
from typing import Any, Dict, Tuple, TypedDict

from eth_account import Account

from pythonsdk.exceptions import ErrInvalidSide, ErrInvalidSymbolFormat, ErrInvalidToken
from pythonsdk.signer import Signer
from pythonsdk.types import CreateOrderInput
from pythonsdk.utils import convert_to_base_unit


class Token(TypedDict):
    address: str
    decimals: int


class OrderSigner(Signer):
    __account: Account

    def __init__(self, private_key: str):
        super().__init__()

        self.__account = Account.from_key(private_key)

    def prepare_and_sign_order(self, order: CreateOrderInput) -> (str, dict):
        """Prepare EIP-712 message and sign it.

        Args:
            order: Order to sign.

        Returns:
            Tuple of signature and EIP712 message data (needed for signature validation)
        """
        in_token, out_token = self.__get_token_details(
            symbol=order["symbol"], side=order["side"]
        )

        domain_data = self._construct_domain_data()
        message_types = self._construct_message_types()
        message_data = self._construct_message_data(
            in_token=in_token,
            out_token=out_token,
            size=order["size"],
            price=order["price"],
            side=order["side"],
            signer_address=self.__account.address,
        )

        signable_message = self.encode_typed_data(
            primary_type="PermitWitnessTransferFrom",
            domain_data=domain_data,
            message_types=message_types,
            message_data=message_data,
        )

        signature = self.sign_message(signable_message, self.__account.key)

        return signature.signature.hex(), message_data

    def _construct_domain_data(self) -> Dict[str, Any]:
        return {
            "name": "Permit2",
            "chainId": 137,
            "verifyingContract": "0x000000000022d473030f116ddee9f6b43ac78ba3",
        }

    def _construct_message_types(self) -> dict:
        return {
            "PermitWitnessTransferFrom": [
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
    ) -> dict:
        in_amount = self.__calculate_in_amount(
            size=size, price=price, side=side, decimals=in_token["decimals"]
        )

        out_amount = self.__calculate_out_amount(
            size=size, price=price, side=side, decimals=out_token["decimals"]
        )
        nonce = random.randint(0, 2**32 - 1)

        deadline = datetime.datetime.now() + datetime.timedelta(days=90)
        epoch_deadline = int(deadline.timestamp())

        return {
            "permitted": {"token": in_token["address"], "amount": str(in_amount)},
            "spender": "0x21Da9737764527e75C17F1AB26Cb668b66dEE0a0",
            "nonce": nonce,
            "deadline": epoch_deadline,
            "witness": {
                "info": {
                    "reactor": "0x21Da9737764527e75C17F1AB26Cb668b66dEE0a0",
                    "swapper": "0xE3682CCecefBb3C3fe524BbFF1598B2BBaC0d6E3",
                    "nonce": nonce,
                    "deadline": epoch_deadline,
                    "additionalValidationContract": "0x1a08D64Fb4a7D0b6DA5606A1e4619c147C3fB95e",
                    "additionalValidationData": "0x",
                },
                "exclusiveFiller": "0x1a08D64Fb4a7D0b6DA5606A1e4619c147C3fB95e",
                "exclusivityOverrideBps": 0,
                "input": {"token": in_token["address"], "amount": str(in_amount)},
                "outputs": [
                    {
                        "token": out_token["address"],
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

        with resources.open_text("pythonsdk", "supportedTokens.json") as f:
            tokens = json.load(f)

        in_token = tokens.get(in_token_symbol)
        out_token = tokens.get(out_token_symbol)

        if not in_token:
            raise ErrInvalidToken(f"Invalid 'in' token symbol: {in_token_symbol}.")

        if not out_token:
            raise ErrInvalidToken(f"Invalid 'out' token symbol: {out_token_symbol}.")

        return in_token, out_token

    def __calculate_in_amount(
        self, *, size: str, price: str, side: str, decimals: int
    ) -> int:
        if side == "buy":
            return convert_to_base_unit(
                token_amount=(float(size) * float(price)),
                decimals=decimals,
            )
        else:
            return convert_to_base_unit(
                token_amount=float(size),
                decimals=decimals,
            )

    def __calculate_out_amount(
        self, *, size: str, price: str, side: str, decimals: int
    ) -> int:
        if side == "sell":
            return convert_to_base_unit(
                token_amount=(float(size) * float(price)),
                decimals=decimals,
            )
        else:
            return convert_to_base_unit(
                token_amount=float(size),
                decimals=decimals,
            )
