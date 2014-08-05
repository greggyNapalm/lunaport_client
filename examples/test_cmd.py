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

#EPOINT = 'http://gkom_IZD5VL1EcLc2lTp:Ge53gsRSs0gej9o@dev.lunaport.domain.ru'

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
    "headers": "[User-Agent:Phantom_0.14.0]\n[Host:target.domain]\n[Connection:close]",
    "address": "87.250.237.140",
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
    "task": "ssb-1693",
    "job_dsc": "XXX test",
    "operator": "lunapark",
    "job_name": "XXX test"
  },
  "lunaport": {
    "case": "gkomissarov1_sandbox",
    "tank_fqdn": [],
    "initiator": "firebat"
  },
}

def main():
    lunaport_c = LunaportClinetV1()
    #lunaport_c = LunaportClinetV1(epoint=EPOINT)
    #lunaport_c = LunaportClinetV1()
    usrers = lunaport_c.user_get_names_butch()
    pp(usrers)
    #src_case = lunaport_c.case_get(66)
    #for u in usrers:
    #    dst_case = {
    #        'name': '{}_sandbox'.format(u),
    #        'descr': src_case['descr'],
    #        'oracle': src_case['oracle'],
    #    }
    #lunaport_c1.case_post(dst_case)
    #    pp(dst_case)

    #rv = lunaport_c.server_put(H_TO_PUT)

    #rv = lunaport_c.dc_get(10)
    #rv = lunaport_c.dc_post({'name': 'created' + str(time.time())})
    #rv = lunaport_c.dc_put({'name': 'puted_at_1400250308.27'})

    #rv = lunaport_c.notifctn_get('sandbox')
    #rv = lunaport_c.test_post_api(new_load_test)
    #pp(rv)
    #rv = lunaport_c.line_get(2345)
    #rv = lunaport_c.line_post({'id': 9876, 'name': 'red2'})
    #rv = lunaport_c.line_put({'id': 9876, 'name': 'red2-222'})
    #ora = json.loads('[{"kw":{"tag":"all"},"name":"assert_resp_times_distr","arg":[99,">",1]}]')

    #rv = lunaport_c.case_post({
    #    'name': 'test-123',
    #    'descr': 'test123',
    #    'oracle': ora,

    #})

    #pp(rv)
    print 'Done'

if __name__ == '__main__':
    main()
