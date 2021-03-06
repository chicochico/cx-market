import time

import pytest
from fastapi.testclient import TestClient
from market.market import app


@pytest.fixture
def client():
    return TestClient(app)


# isin (String, 12 chars (this identifies a stock))
# limit_price (Float, always >0)
# side (Enum: buy | sell, case sensitive tolerant)
# valid_until (Integer, Unix UTC Timestamp)
# quantity (Integer, always >0)

valid_until_timestamp = int(time.time()) + (60 * 60 * 24)

valid_orders = [
    {
        "isin": "US0378331005",
        "limit_price": 130.0,
        "side": "buy",
        "valid_until": valid_until_timestamp,
        "quantity": 200,
    },
    {
        "isin": "US0378331005",
        "limit_price": 150.0,
        "side": "sell",
        "valid_until": valid_until_timestamp,
        "quantity": 200,
    },
    {
        "isin": "US36467W1099",
        "limit_price": 11.0,
        "side": "Sell",  # uppercase
        "valid_until": valid_until_timestamp,
        "quantity": 30,
    },
    {
        "isin": "US36467W1099",
        "limit_price": 11.0,
        "side": "Buy",  # uppercase
        "valid_until": valid_until_timestamp,
        "quantity": 30,
    },
    {
        "isin": "NL0010273215",
        "limit_price": 560.0,
        "side": "sell",
        "valid_until": valid_until_timestamp,
        "quantity": 100,
    },
    {
        "isin": "NL0010273215",
        "limit_price": 540.0,
        "side": "buy",
        "valid_until": valid_until_timestamp,
        "quantity": 100,
    },
]


invalid_orders = [
    {
        "isin": "US0378331005",
        "limit_price": 0,  # invalid price
        "side": "buy",
        "valid_until": valid_until_timestamp,
        "quantity": 200,
    },
    {
        "isin": "US0378331005",
        "limit_price": 150.0,
        "side": "sell",
        "valid_until": valid_until_timestamp,
        "quantity": -10,  # invalid quantity
    },
    {
        "isin": "US36467W1099",
        "limit_price": 11.0,
        "side": "foobar",  # invalid side
        "valid_until": valid_until_timestamp,
        "quantity": 30,
    },
    {
        "isin": "RANDOMISIN",  # invalid isin
        "limit_price": 11.0,
        "side": "Buy",  # uppercase
        "valid_until": valid_until_timestamp,
        "quantity": 30,
    },
    {
        "isin": "US36467W10990001",  # invalid isin
        "limit_price": 11.0,
        "side": "Buy",  # uppercase
        "valid_until": valid_until_timestamp,
        "quantity": 30,
    },
    {
        "isin": 100,  # integer isin
        "limit_price": 11.0,
        "side": "Buy",  # uppercase
        "valid_until": valid_until_timestamp,
        "quantity": 30,
    },
    {
        "isin": "NL0010273215",
        "limit_price": 560.0,
        "side": "sell",
        "valid_until": 1619647112,  # in the past
        "quantity": 100,
    },
    {
        "isin": "NL0010273215",
        "limit_price": -540.0,
        "side": "buy",
        "valid_until": valid_until_timestamp,
        "quantity": 100,
    },
    # missing fields
    {
        "limit_price": 540.0,
        "side": "buy",
        "valid_until": valid_until_timestamp,
        "quantity": 100,
    },
    {
        "isin": "NL0010273215",
        "side": "buy",
        "valid_until": valid_until_timestamp,
        "quantity": 100,
    },
    {
        "isin": "NL0010273215",
        "limit_price": -540.0,
        "valid_until": valid_until_timestamp,
        "quantity": 100,
    },
    {
        "isin": "NL0010273215",
        "limit_price": -540.0,
        "side": "buy",
        "quantity": 100,
    },
    {
        "isin": "NL0010273215",
        "limit_price": -540.0,
        "side": "buy",
        "valid_until": valid_until_timestamp,
    },
    {},
]


@pytest.mark.parametrize(
    "test_input",
    valid_orders,
)
def test_valid_orders(client, test_input):
    response = client.post("/orders/order", json=test_input)
    assert response.status_code == 200
    assert response.json() == {"msg": "success"}


@pytest.mark.parametrize(
    "test_input",
    invalid_orders,
)
def test_invalid_orders(client, test_input):
    response = client.post("/orders/order", json=test_input)
    assert response.status_code == 422  # validation error


def test_get_orders(client):
    response = client.get("/orders")
    assert response.status_code == 200
    assert len(response.json()) == 6  # the 6 orders submitted in the valid orders test
