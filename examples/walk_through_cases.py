#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    lunaport_worker.tasks.hosts_mgmt_cmd
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Smoke test for whole system.
"""

import json
import time
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

from lunaport_client.http_client import LunaportClinetV1 
from lunaport_client.exceptions import LunaportClientError

#EPOINT = 'http://gkom_IZD5VL1EcLc2lTp:Ge53gsRSs0gej9o@dev.lunaport.domain'

H_TO_CREATE = {
    'fqdn': 'firebat.domain.ru'
}

H_TO_PATCH = {
    'fqdn': 'firebat.domain.ru',
    "is_spec_tank": False,
    "is_tank": False,
    "descr": "X O X O"
}

H_TO_PUT = {
    'fqdn': 'firebat.domain.ru',
    "is_spec_tank": True,
    "is_tank": True,
}


new_load_test = {
  "phantom": {
    "ssl": "0",
    "header_http": "1.1",
    "writelog": "all",
    "ammofile": "/var/bmpt/gkomissarov/ammo/file.qs.gz",
    "headers": "[User-Agent:Phantom_0.14.0]\n[Host:target]\n[Connection:close]",
    "address": "8.8.8.8",
    "instances": "10000",
    "port": "36255",
    "rps_schedule": "line(1, 15, 1m)"
  },
  "monitoring": {
    "config": "none"
  },
  "aggregator": {
    "time_periods": "45 50 100 150 200 250 300 350 400 450 500 600 700 800 900 1s 2s 3s 4s 5s 6s 7s 8s 9s 10s"
  },
  "meta": {
    "task": "tasktt",
    "job_dsc": "XXX test",
    "operator": "napalm",
    "job_name": "XXX test"
  },
  "lunaport": {
    "case": "napalm_sandbox",
    "tank_fqdn": [],
    "initiator": "firebat"
  },
}



def hndl_oracle(ora):
    pass

def main():
    lunaport_c = LunaportClinetV1()
    cases = lunaport_c.case_get_names_butch()

    BAD_ORA = lunaport_c.case_get(66)['oracle']
    pp(BAD_ORA)
    for (c_id, c_name) in cases:
        print c_id,
        if c_id != 66:
            print 'BAD ORA'
            continue
        case = lunaport_c.case_get(c_id)
        if case['oracle'] == BAD_ORA:
            print '1'
            diff = {
                'oracle': [BAD_ORA]
            }
            lunaport_c.case_patch(c_id, diff)
        else:
            print '0'


if __name__ == '__main__':
    main()
