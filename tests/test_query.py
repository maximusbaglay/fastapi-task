import pytest

@pytest.mark.parametrize("ticker", ["SBER", "GAZP"])
def test_get_data_by_ticker(ticker):
    get_data_by_ticker()