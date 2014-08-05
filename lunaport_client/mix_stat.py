# -*- encoding: utf-8 -*-

"""
    lunaport_client.v1.stat
    ~~~~~~~~~~~~~~~~~~~~~~~

    Stat(Load test result statistic) REST resource.
"""

import json
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

import requests

from exceptions import panic


class Stat(object):
    def stat_get(self, test_id, ammo_tag='all'):
        resp = None
        url = '{}tests/{}/stat/{}'.format(self.epoint, test_id, ammo_tag)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def stat_get_avail(self, test_id):
        """Get list of avaliable statistics for test.
        """
        resp = None
        url = '{}tests/{}/stat/'.format(self.epoint, test_id)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def stat_post(self, test_id, ammo_tag, ver, doc):
        resp = None
        codes_allowed = [201, ]
        url = '{}tests/{}/stat/{}'.format(self.epoint, test_id, ammo_tag)
        body_json = json.dumps({
            'version': ver,
            'doc': doc,
        })
        try:
            resp = requests.post(url, timeout=self.to, headers=self.headers, data=body_json)
        except Exception as e:
            panic(e=e, resp=resp)

        if resp.status_code not in codes_allowed:
            panic(resp=resp)
        return resp.json()
