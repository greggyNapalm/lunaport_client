# -*- encoding: utf-8 -*-

"""
    lunaport_client.v1.case
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Case REST resource.
"""

import json
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

import requests

from exceptions import panic


class Case(object):
    case_attrs_allowed = [
        'name',
        'descr',
        'oracle',
    ]

    def case_get(self, case_id):
        resp = None
        url = '{}case/{}'.format(self.epoint, case_id)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def case_post(self, case):
        resp = None
        codes_allowed = [201, ]
        url = '{}case/'.format(self.epoint)
        body_json = json.dumps(self.fillter_dct(self.case_attrs_allowed, case))
        try:
            resp = requests.post(url, timeout=self.to, headers=self.headers,
                                 data=body_json)
        except Exception as e:
            panic(e=e, resp=resp)

        if resp.status_code not in codes_allowed:
            panic(resp=resp)
        return resp.json(), resp.headers.get('location')

    def case_get_names_butch(self):
        resp = None
        url = '{}case/?names_butch=true'.format(self.epoint)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def case_patch(self, case_id, diff):
        """
        Patch existing case entrie.
        Args:
            case_id: int
            diff: dict

        Returns:
            dict: New case entrie respresentation.

        Throws:
            LunaportClientError
        """
        resp = None
        url = '{}case/{}'.format(self.epoint, case_id)
        try:
            resp = requests.patch(url, data=json.dumps(diff), headers=self.headers)
            resp.raise_for_status()
            return resp.json(), resp.headers.get('location')
        except Exception as e:
            panic(e=e, resp=resp)
