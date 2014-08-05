#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    app.module
    ~~~~~~~~~~~~~~~
    
    Some info about this module.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pprint
pp = pprint.PrettyPrinter(indent=4)

from lunaport_client.lunaport import LunaportClinet
from lunaport_client.exceptions import LunaportClientError

AUTH = ('fake-user', 'fake-passwd')
load_cfg_path = '/Users/gkomissarov/Downloads/examples/feuer.ini'
phout_path = '/Users/gkomissarov/Downloads/examples/phout.log'
TEST_META = {
    'load_src': 'generator.domain',
    'env': 'yandex-tank',
    'case': 'usr-napalm-dev',
    'initiator': 'firebat',
}

def read_f(f_path):
    """Read whole file from local fs, wraps errors with ..."""
    with open(f_path, 'r') as fh:
        rv = fh.read()
    return rv

def main():
    load_cfg = read_f(load_cfg_path) 
    phout = read_f(phout_path)
    c = LunaportClinet(auth=AUTH)
    try:
        rv = c.create_from_arts(TEST_META, load_cfg, phout)
    except LunaportClientError as e:
        print (e)
        return 
    pp.pprint(rv)

if __name__ == '__main__':
    main()
