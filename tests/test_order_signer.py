import pytest

from orbs_orderbook import OrderSigner


@pytest.mark.parametrize(
    "size, price, side, decimals, expected",
    [
        ("40", "0.87", "sell", 6, 34800000),
        ("123734734873497834", 1, "sell", 6, 123734734873497834000000),
        ("543", "0.09", "sell", 6, 48870000),
        ("40", "0.87", "buy", 6, 40000000),
        ("123734734873497834", 1, "buy", 6, 123734734873497834000000),
        ("543", "0.09", "buy", 6, 543000000),
    ],
)
def test_calculate_out_amount(mocker, size, price, side, decimals, expected):
    client = mocker.Mock()
    signer = OrderSigner(
        private_key="0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        sdk=client,
    )

    in_amount = signer._calculate_out_amount(
        size=size, price=price, side=side, decimals=decimals
    )

    assert in_amount == expected, "Incorrect out amount"


@pytest.mark.parametrize(
    "size, price, side, decimals, expected",
    [
        ("40", "0.87", "buy", 6, 34800000),
        ("123734734873497834", 1, "buy", 6, 123734734873497834000000),
        ("543", "0.09", "buy", 6, 48870000),
        ("40", "0.87", "sell", 6, 40000000),
        ("123734734873497834", 1, "sell", 6, 123734734873497834000000),
        ("543", "0.09", "sell", 6, 543000000),
    ],
)
def test_calculate_in_amount(mocker, size, price, side, decimals, expected):
    client = mocker.Mock()
    signer = OrderSigner(
        private_key="0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        sdk=client,
    )

    in_amount = signer._calculate_in_amount(
        size=size, price=price, side=side, decimals=decimals
    )

    assert in_amount == expected, "Incorrect out amount"
