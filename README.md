# Python SDK for Orb's order book

This Python SDK allows you to query the Orb's order book and place orders.

**Please note that this SDK is still in development and is subject to change.**

## Getting started

The SDK [is available on PyPI](https://pypi.org/project/orbs-orderbook-sdk/) and can be installed with `pip`:

```bash
pip install orbs-orderbook-sdk
```

You will need to request an API key from the Orbs team, and provide us with your Externally Owned Account (EOA) wallet address (NOT the private key).

## Usage

### Creating an order

See `examples/create_order.py`.

### Signing an order

See `examples/sign_order.py`.

### Cancelling orders

See `examples/cancel_order.py`.

### Getting orders (open and filled)

See `examples/get_orders.py`.

## Folder structure

- `examples`: Example scripts
- `orbs_orderbook`: The Python SDK source code

## Development

### Installation

1. Ensure you have at least Python 3.8 installed

#### Pip

1. Run `pip install -r requirements.txt` to install dependencies

#### Poetry

1. Install [Poetry](https://python-poetry.org/docs/#installation)
1. Run `poetry install` to install dependencies into a virtual environment
