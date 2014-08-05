# -*- encoding: utf-8 -*-

"""
    lunaport_client.v1.line
    ~~~~~~~~~~~~~~~~~~~~~~~

    Line(mean power line - district of datacenter) REST resource
"""

import json
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

import requests

from exceptions import panic


class Line(object):
    line_attrs_allowed = [
        'id',
        'name',
    ]

    def line_get(self, line_id):
        resp = None
        url = '{}line/{}'.format(self.epoint, line_id)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def line_post(self, line):
        resp = None
        codes_allowed = [201, ]
        url = '{}line/'.format(self.epoint)
        body_json = json.dumps(self.fillter_dct(self.line_attrs_allowed, line))
        try:
            resp = requests.post(url, timeout=self.to, headers=self.headers,
                                 data=body_json)
        except Exception as e:
            panic(e=e, resp=resp)

        if resp.status_code not in codes_allowed:
            panic(resp=resp)
        return resp.json(), resp.headers.get('location')

    def line_put(self, line):
        """ Try to update existing line entrie, insert on fail.
        Args:
            line: dict, @see line_attrs_allowed.

        Returns:
            resource representation - dict, resource location - str
        """
        resp = None
        url = '{}line/'.format(self.epoint)
        body_json = json.dumps(self.fillter_dct(self.line_attrs_allowed, line))
        try:
            resp = requests.put(url, timeout=self.to, headers=self.headers,
                                data=body_json)
            resp.raise_for_status()
        except Exception as e:
            panic(e=e, resp=resp)

        return resp.json(), resp.headers.get('location')
