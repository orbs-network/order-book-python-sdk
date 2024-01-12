"""Get order examples
Includes getting single order, all open orders, and all filled (closed) orders
"""

import asyncio
import os

from orbs_orderbook import OrderBookSDK

BASE_URL = os.environ.get("BASE_URL", "http://localhost")


async def main():
    client = OrderBookSDK(base_url=BASE_URL, api_key="og4lpqQUILyciacspkFESHE1qrXIxpX1")

    # Get single order by order ID
    order_id = "accfae6b-3a9e-4719-85f0-a34fbc16fb3b"
    client.get_order_by_id(order_id=order_id)

    # Get single order by client order ID
    client_oid = "550e8400-e29b-41d4-a716-446655440000"
    client.get_order_by_client_id(client_order_id=client_oid)

    # Get all open orders (paginated)
    client.get_orders_for_user(page=1, page_size=10)

    # Get all filled orders (paginated)
    client.get_filled_orders_for_user(page=1, page_size=10)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
