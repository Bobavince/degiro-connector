# IMPORTATIONS STANDARD
import logging

# IMPORTATION THIRD PARTY
import pytest
import urllib3

# IMPORTATION INTERNAL
from degiro_connector.trading.api import API as TradingAPI

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# TESTS FIXTURES
@pytest.mark.trading
def test_fixture_trading(trading):
    assert isinstance(trading, TradingAPI)


@pytest.mark.network
@pytest.mark.trading
def test_fixture_trading_connected(trading_connected):
    session_id = trading_connected.connection_storage.session_id

    assert isinstance(session_id, str)
    assert len(session_id) == 45
