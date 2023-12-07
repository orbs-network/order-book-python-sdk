"""Sign an order"""

import asyncio
import random

from eth_account import Account
from eth_account.messages import encode_typed_data

from pythonsdk.order_signer import OrderSigner
from pythonsdk.types import CreateOrderInput
from pythonsdk.utils import convert_to_base_unit


async def main():
    pk = "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    order_signer = OrderSigner(pk)

    signature, message_data_str = order_signer.prepare_and_sign_order(
        CreateOrderInput(
            price="20000",
            size="20",
            symbol="WBTC-USDC",
            side="sell",
            clientOrderId="a677273e-12de-4acc-a4f8-de7fb5b86e37",
        )
    )

    print("signature: ", signature)
    print("message_data_str: ", message_data_str)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
