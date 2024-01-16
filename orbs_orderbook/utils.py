from decimal import Decimal

from web3 import Web3

from orbs_orderbook.types import Base


def hash_string(value: str):
    return Web3.solidity_keccak(["string"], [value]).hex()


def convert_to_base_unit(*, token_amount: Decimal, decimals: int):
    """
    Convert an amount of tokens to the base unit.

    :param token_amount: The amount of tokens to be converted.
    :param decimals: The number of decimals the token uses.
    :return: The amount (in the token's smallest unit).
    """
    multiplier = Decimal(10) ** decimals
    return int(token_amount * multiplier)


def dataclass_serializer(obj):
    if isinstance(obj, Base):
        return obj.to_camelcase_dict()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
