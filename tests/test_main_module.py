import os
import pytest
from binance.client import Client
from src.enums.enums import ErrorMessage


@pytest.mark.parametrize('symbol, result', [
    ('BTCUSDT', True),
    ])
def test_get_price(symbol, result):
    client = Client(api_key=os.getenv('API_KEY'), api_secret=os.getenv('SECRET_KEY'))
    ticker = client.get_symbol_ticker(symbol=symbol)
    pair_price = float(ticker['price'])
    assert isinstance(pair_price, float) == result, ErrorMessage.WRONG_INSTANCE_RESULT.value

@pytest.mark.parametrize('symbol, result', [
    ('vhdvb', 400),
    ('456132', 400)
])
def test_get_price_negative(symbol, result):
    client = Client(api_key=os.getenv('API_KEY'), api_secret=os.getenv('SECRET_KEY'))
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
    except Exception as e:

        assert e.status_code == result, ErrorMessage.WRONG_STATUS_CODE.value

@pytest.mark.parametrize('volume, divider, result', [
    (10.0, 2, 5.0)
])
def test_calculate_volume(volume, divider, result):
    assert volume / divider == result, ErrorMessage.WRONG_INSTANCE_RESULT.value

@pytest.mark.parametrize('volume, divider, result', [
    (10.0, 0, ZeroDivisionError)
])
def test_calculate_volume_negative(volume, divider, result):
    try:
        volume / divider
    except Exception as e:
        assert e.__class__ == result, ErrorMessage.WRONG_ERROR_CLASS.value

@pytest.mark.parametrize('main_value, additional_value, result', [
    (100.0, 10, True),
    (0, 10, False)
]
                         )
def test_set_price(main_value, additional_value, result):
    assert isinstance((main_value + additional_value), float) == result, ErrorMessage.WRONG_INSTANCE_RESULT.value
