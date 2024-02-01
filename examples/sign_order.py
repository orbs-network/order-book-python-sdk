"""Sign an order"""

import asyncio
import os

from eth_account import Account
from eth_account.messages import encode_typed_data

from orbs_orderbook import CreateOrderInput, OrderBookSDK, OrderSigner

BASE_URL = os.environ.get("BASE_URL", "http://localhost")
API_KEY = os.environ.get("API_KEY", "38052ba1012aa665458cf2d28b9d057d")
PRVIATE_KEY = os.environ.get(
    "PRVIATE_KEY", "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
)


async def main():
    client = OrderBookSDK(base_url=BASE_URL, api_key=API_KEY)
    order_signer = OrderSigner(private_key=PRVIATE_KEY, sdk=client)

    signature, message_data_str = order_signer.prepare_and_sign_order(
        CreateOrderInput(
            price="20000",
            size="20",
            symbol="MATIC-USDC",
            side="sell",
            client_order_id="a677273e-12de-4acc-a4f8-de7fb5b86e37",
        )
    )

    print("signature: ", signature)
    print("message_data_str: ", message_data_str)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
