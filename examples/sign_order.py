"""Sign an order"""

import asyncio
import os

from orbs_orderbook import CreateOrderInput, OrderBookSDK, OrderSigner

BASE_URL = os.environ.get("BASE_URL", "http://localhost")


async def main():
    pk = "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    sdk = OrderBookSDK(base_url=BASE_URL, api_key="ox9xiaYHSzkH7yNKpEPppAoZm33Yurbd")
    order_signer = OrderSigner(pk, sdk)

    signature, message = order_signer.prepare_and_sign_order(
        CreateOrderInput(
            price="0.86500000",
            size="40",
            symbol="MATIC-USDC",
            side="sell",
            client_order_id="550e8400-e29b-41d4-a716-446655440000",
        )
    )

    print("signature: ", signature)
    print("message: ", message)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
