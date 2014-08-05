# -*- encoding: utf-8 -*-

"""
    lunaport_client.v1.dc
    ~~~~~~~~~~~~~~~~~~~~~

    Dc(datacenter) REST resource.
"""

import json
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

import requests

from exceptions import panic


class Dc(object):
    dc_attrs_allowed = [
        'name'
    ]

    def dc_get(self, dc_id):
        resp = None
        url = '{}dc/{}'.format(self.epoint, dc_id)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def dc_post(self, dc):
        resp = None
        codes_allowed = [201, ]
        url = '{}dc/'.format(self.epoint)
        body_json = json.dumps(self.fillter_dct(self.dc_attrs_allowed, dc))
        try:
            resp = requests.post(url, timeout=self.to, headers=self.headers,
                                 data=body_json)
        except Exception as e:
            panic(e=e, resp=resp)

        if resp.status_code not in codes_allowed:
            panic(resp=resp)
        return resp.json(), resp.headers.get('location')

    def dc_put(self, dc):
        """ Try to update existing dc entrie, insert on fail.
        Args:
            dc: dict, @see dc_attrs_allowed.

        Returns:
            resource representation - dict, resource location - str
        """
        resp = None
        url = '{}dc/'.format(self.epoint)
        body_json = json.dumps(self.fillter_dct(self.dc_attrs_allowed, dc))
        try:
            resp = requests.put(url, timeout=self.to, headers=self.headers,
                                data=body_json)
            resp.raise_for_status()
        except Exception as e:
            panic(e=e, resp=resp)

        return resp.json(), resp.headers.get('location')
