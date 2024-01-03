from decimal import Decimal
from web3 import Web3


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
