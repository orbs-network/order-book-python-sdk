"""Batch create orders"""

import asyncio
import os

from orbs_orderbook import (
    CreateOrderInput,
    OrderBookSDK,
    OrderSigner,
    OrderWithSignature,
    CreateMultipleOrdersInput,
)

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

    order_one = CreateOrderInput(
        price="0.86500000",
        size="40",
        symbol="MATIC-USDC",
        side="buy",
        client_order_id="550e8400-e29b-41d4-a716-446655440000",
    )
    order_one_sig, order_one_msg = signer.prepare_and_sign_order(order_one)

    order_two = CreateOrderInput(
        price="0.87",
        size="40",
        symbol="MATIC-USDC",
        side="sell",
        client_order_id="650e8400-e29b-41d4-a716-446655440001",
    )
    order_two_sig, order_two_msg = signer.prepare_and_sign_order(order_two)

    create_orders_input = CreateMultipleOrdersInput(
        # Orders must be for the same symbol
        symbol="MATIC-USDC",
        # You may specify up to 10 orders
        orders=[
            OrderWithSignature(
                order=order_one,
                signature=order_one_sig,
                message=order_one_msg,
            ),
            OrderWithSignature(
                order=order_two,
                signature=order_two_sig,
                message=order_two_msg,
            ),
        ],
    )

    res = client.create_multiple_orders(create_orders_input)

    print(f"Create multiple orders response: {res}")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
