"""Create a new order"""

import asyncio
import os

from orbs_orderbook import CreateOrderInput, OrderBookSDK, OrderSigner

BASE_URL = os.environ.get("BASE_URL", "http://localhost")
API_KEY = os.environ.get("API_KEY", "38052ba1012aa665458cf2d28b9d057d")
PRVIATE_KEY = os.environ.get(
    "PRVIATE_KEY", "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
)


async def main():
    client = OrderBookSDK(base_url=BASE_URL, api_key=API_KEY)
    signer = OrderSigner(
        private_key=PRVIATE_KEY,
        sdk=client,
    )

    order_input = CreateOrderInput(
        price="0.86500000",
        size="40",
        symbol="MATIC-USDC",
        side="sell",
        client_order_id="550e8400-e29b-41d4-a716-446655440000",
    )

    # You may specify a custom signature expiration time (`deadline`). If not specified, the default is 1 day.
    signature, message = signer.prepare_and_sign_order(order_input)

    res = client.create_order(
        order_input=order_input,
        signature=signature,
        message=message,
    )

    print(f"Create order response: {res}")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
