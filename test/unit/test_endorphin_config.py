import pytest
import os
import sys
import re
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
os.environ['SENTINEL_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from endorphin_config import EndorphinConfig


@pytest.fixture
def endorphin_conf(**kwargs):
    defaults = {
        'rpcuser': 'endorphinrpc',
        'rpcpassword': 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk',
        'rpcport': 29241,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(**defaults)

    return conf


def test_get_rpc_creds():
    endorphin_config = endorphin_conf()
    creds = EndorphinConfig.get_rpc_creds(endorphin_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'endorphinrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 29241

    endorphin_config = endorphin_conf(rpcpassword='s00pers33kr1t', rpcport=8000)
    creds = EndorphinConfig.get_rpc_creds(endorphin_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'endorphinrpc'
    assert creds.get('password') == 's00pers33kr1t'
    assert creds.get('port') == 8000

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', endorphin_conf(), re.M)
    creds = EndorphinConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'endorphinrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 19998


# ensure endorphin network (mainnet, testnet) matches that specified in config
# requires running endorphind on whatever port specified...
#
# This is more of a endorphind/jsonrpc test than a config test...
