# -*- encoding: utf-8 -*-

"""
    lunaport_client.v1.server
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Server(load srs or load dest host) REST resource.
"""

import json
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

import requests

from exceptions import panic


class Server(object):
    server_attrs_allowed = [
        'fqdn',
        'descr',
        'dc',
        'is_spec_tank',
        'is_tank',
        'host_serv',
        'line_name'
    ]

    def server_get(self, fqdn):
        resp = None
        url = '{}host/{}'.format(self.epoint, fqdn)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def server_get_names_butch(self):
        resp = None
        url = '{}host/?names_butch=true'.format(self.epoint)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def server_post(self, server):
        resp = None
        codes_allowed = [201, ]
        url = '{}host/'.format(self.epoint)
        body_json = json.dumps(self.fillter_dct(self.server_attrs_allowed, server))
        try:
            resp = requests.post(url, timeout=self.to, headers=self.headers,
                                 data=body_json)
        except Exception as e:
            panic(e=e, resp=resp)

        if resp.status_code not in codes_allowed:
            panic(resp=resp)
        return resp.json(), resp.headers.get('location')

    def server_patch(self, fqdn, diff):
        """ Try to update existing server entrie, insert on fail.
        Args:
            fqdn: str, uniq server attribute.
            server: dict, @see server_attrs_allowed.

        Returns:
            resource representation - dict, resource location - str
        """
        resp = None
        url = '{}host/{}'.format(self.epoint, fqdn)
        body_json = json.dumps(self.fillter_dct(self.server_attrs_allowed, diff))
        try:
            resp = requests.patch(url, timeout=self.to, headers=self.headers,
                                  data=body_json)
            resp.raise_for_status()
        except Exception as e:
            panic(e=e, resp=resp)

        return resp.json(), resp.headers.get('location')

    def server_put(self, server):
        """ Try to update existing server entrie, insert on fail.
        Args:
            server: dict, @see server_attrs_allowed.

        Returns:
            resource representation - dict, resource location - str
        """
        resp = None
        url = '{}host/'.format(self.epoint)
        body_json = json.dumps(self.fillter_dct(self.server_attrs_allowed, server))
        try:
            resp = requests.put(url, timeout=self.to, headers=self.headers,
                                data=body_json)
            resp.raise_for_status()
        except Exception as e:
            panic(e=e, resp=resp)

        return resp.json(), resp.headers.get('location')
