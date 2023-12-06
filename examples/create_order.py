"""Create a new order"""

import asyncio
import os

from pythonsdk.client import OrderBookSDK
from pythonsdk.order_signer import OrderSigner
from pythonsdk.types import CreateOrderInput

BASE_URL = os.environ.get("BASE_URL", "http://localhost")


async def main():
    client = OrderBookSDK(base_url=BASE_URL, api_key="38052ba1012aa665458cf2d28b9d057d")
    signer = OrderSigner(
        private_key="0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    )

    order_input = CreateOrderInput(
        price="2000",
        size="10",
        symbol="ETH-USDC",
        side="buy",
        clientOrderId="550e8400-e29b-41d4-a716-446655440000",
    )

    signature, message_data = signer.prepare_and_sign_order(order_input)

    res = client.create_order(
        order_input=order_input,
        signature=signature,
        message_data=message_data,
    )

    print(f"Create order response: {res}")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
