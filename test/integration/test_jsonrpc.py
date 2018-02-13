import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from endorphind import EndorphinDaemon
from endorphin_config import EndorphinConfig


def test_endorphind():
    config_text = EndorphinConfig.slurp_config_file(config.endorphin_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000d31b656910f3d611b2cf1917bec57557c163ba89ed522848757a2e50a44'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000f83c051bb110fa1b2e45e14d673d1eb11a6990333e5d2b0e1e6e0154288'

    creds = EndorphinConfig.get_rpc_creds(config_text, network)
    endorphind = EndorphinDaemon(**creds)
    assert endorphind.rpc_command is not None

    assert hasattr(endorphind, 'rpc_connection')

    # Endorphin testnet block 0 hash == 000009110a70cd2bf2cdcae9a8b1425bb074c7b7b08570c2c9f04fe8668c6589
    # test commands without arguments
    info = endorphind.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert endorphind.rpc_command('getblockhash', 0) == genesis_hash
