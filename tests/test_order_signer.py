import pytest

from orbs_orderbook import OrderSigner

from orbs_orderbook.exceptions import ErrDecimalPlaces

from decimal import Decimal


@pytest.mark.parametrize(
    "size, price, side, decimals, expected",
    [
        (Decimal("40"), Decimal("0.87"), "sell", 6, 34800000),
        (
            Decimal("123734734873497834"),
            Decimal("1"),
            "sell",
            6,
            123734734873497834000000,
        ),
        (Decimal("543"), Decimal("0.09"), "sell", 6, 48870000),
        (Decimal("50"), Decimal("0.86440911"), "sell", 6, 43220455),
        (Decimal("40"), Decimal("0.87"), "buy", 6, 40000000),
        (
            Decimal("123734734873497834"),
            Decimal("1"),
            "buy",
            6,
            123734734873497834000000,
        ),
        (Decimal("543"), Decimal("0.09"), "buy", 6, 543000000),
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
        (Decimal("40"), Decimal("0.87"), "buy", 6, 34800000),
        (
            Decimal("123734734873497834"),
            Decimal("1"),
            "buy",
            6,
            123734734873497834000000,
        ),
        (Decimal("543"), Decimal("0.09"), "buy", 6, 48870000),
        (Decimal("50"), Decimal("0.86440911"), "buy", 6, 43220455),
        (Decimal("40"), Decimal("0.87"), "sell", 6, 40000000),
        (
            Decimal("123734734873497834"),
            Decimal("1"),
            "sell",
            6,
            123734734873497834000000,
        ),
        (Decimal("543"), Decimal("0.09"), "sell", 6, 543000000),
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


@pytest.mark.parametrize(
    "price, should_raise",
    [
        (Decimal("0.86"), False),
        (Decimal("22.23"), False),
        (Decimal("1.862"), False),
        (Decimal("0.000003"), False),
        (Decimal("10002.000003"), False),
        (Decimal("0"), False),
        (Decimal("100"), False),
        (Decimal("1.2345678"), False),
        (Decimal("12345678901234567890.12345678"), False),
        (Decimal("0.123456789"), True),
        (Decimal("0.123456789123456789"), True),
        (Decimal("1.000000001"), True),
    ],
)
def test_check_decimal_places(mocker, price, should_raise):
    client = mocker.Mock()
    signer = OrderSigner(
        private_key="0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        sdk=client,
    )

    if should_raise:
        with pytest.raises(ErrDecimalPlaces) as e:
            signer._check_decimal_places(price=price)
    else:
        try:
            signer._check_decimal_places(price=price)
        except ErrDecimalPlaces:
            pytest.fail("Unexpected ErrDecimalPlaces raised")
