"""Cancel order examples
Includes cancelling by client order ID and cancelling all orders
"""

import asyncio
import os

from orbs_orderbook import OrderBookSDK

BASE_URL = os.environ.get("BASE_URL", "http://localhost")
API_KEY = os.environ.get("API_KEY", "38052ba1012aa665458cf2d28b9d057d")


async def main():
    client = OrderBookSDK(base_url=BASE_URL, api_key=API_KEY)

    # Cancel by order ID
    res = client.cancel_order_by_id(order_id="f8e17e12-ffa6-486c-8ba2-8f2fe6fe638f")
    print("Cancel by order ID response:", res)

    # Cancel by client order ID
    res = client.cancel_order_by_client_id(
        client_order_id="550e8400-e29b-41d4-a716-446655440000"
    )
    print("Cancel by client order ID response:", res)

    # Cancel all orders
    res = client.cancel_all_orders()
    print("Cancel all orders response:", res)

    # Cancel all orders for a specific symbol
    res = client.cancel_all_orders_by_symbol(symbol="MATIC-USDC")
    print("Cancel all orders by symbol response:", res)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
