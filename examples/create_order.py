import os
import time

from pythonsdk.client import OrderBookSDK
from pythonsdk.types import PlaceOrderInput

import asyncio

BASE_URL = os.environ.get("BASE_URL", "http://localhost")


async def main():
    client = OrderBookSDK(base_url=BASE_URL, api_key="38052ba1012aa665458cf2d28b9d057d")

    order_input = PlaceOrderInput(
        price="10000",
        size="10",
        symbol="USDC-ETH",
        side="sell",
        clientOrderId="550e8400-e29b-41d4-a716-446655440000",
    )

    signature = "0x6e0e553b220cdc66646adf11ca929dfdcd69e410c1389ff2436c7e44bce7eb9c08f41336d2a8cff599acf80f7d3e120019e3006c74978ba3ed1b2ff82e093e4e1c"
    timestamp = str(int(time.time()))

    res = client.place_order(
        order_input=order_input,
        signature=signature,
        timestamp=timestamp,
    )

    print(f"Place order response: {res}")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
