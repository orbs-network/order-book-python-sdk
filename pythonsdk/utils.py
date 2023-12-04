from web3 import Web3


def hash_string(value: str):
    return Web3.solidity_keccak(["string"], [value]).hex()


def convert_to_base_unit(*, token_amount: float, decimals: int):
    """
    Convert an amount of tokens to the base unit.

    :param token_amount: The amount of tokens to be converted.
    :param decimals: The number of decimals the token uses.
    :return: The amount in the token's base unit.
    """
    return int(token_amount * (10**decimals))
