"""Cancel order examples
Includes cancelling by client order ID and cancelling all orders
"""

import asyncio
import os

from pythonsdk import OrderBookSDK

BASE_URL = os.environ.get("BASE_URL", "http://localhost")


async def main():
    client = OrderBookSDK(base_url=BASE_URL, api_key="abc123")

    # Cancel by order ID
    res = client.cancel_order_by_id(order_id="546d10cf-e5ea-4ff7-82ce-6dd1c8cb8c6b")
    print("Cancel by order ID response:", res)

    # Cancel by client order ID
    res = client.cancel_order_by_client_id(
        client_order_id="85f9b615-7f23-4bfb-be4b-9dcb0bde33b7"
    )
    print("Cancel by client order ID response:", res)

    # Cancel all orders
    res = client.cancel_all_orders()
    print("Cancel all orders response:", res)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
