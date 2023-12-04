from typing import Any, Dict, Union

from eth_account import Account
from eth_account.messages import SignableMessage, encode_typed_data
from eth_keys import keys
from eth_typing import HexStr


class Signer:
    def __init__(self):
        pass

    def encode_typed_data(
        self,
        *,
        primary_type: str,
        domain_data: Dict[str, Any],
        message_types: Dict[str, Any],
        message_data: Dict[str, Any],
    ):
        """
        Encodes typed data according to EIP-712 standards.
        """
        return encode_typed_data(
            full_message={
                "primaryType": primary_type,
                "domain": domain_data,
                "types": message_types,
                "message": message_data,
            }
        )

    def sign_message(
        self,
        signable_message: SignableMessage,
        private_key: Union[bytes, HexStr, int, keys.PrivateKey],
    ):
        """
        Signs the message and returns the signature.
        """

        return Account.sign_message(signable_message, private_key)
