# -*- encoding: utf-8 -*-

"""
    lunaport_client.v1.proj
    ~~~~~~~~~~~~~~~~~~~~~~~

    Proj(copied from issue tracker project entrie) REST resource.
"""

import json
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

import requests

from exceptions import panic


class Proj(object):
    def proj_get(self, proj_name):
        resp = None
        url = '{}proj/{}'.format(self.epoint, proj_name)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def proj_get_names_butch(self):
        resp = None
        url = '{}proj/?names_butch=true'.format(self.epoint)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)


    def proj_post(self, proj_name):
        """ All meta data will be fetched from issue tracker if possible.
        """
        resp = None
        codes_allowed = [201,]
        url = '{}proj/'.format(self.epoint)
        body_json = json.dumps({
            'name': proj_name,
        })
        try:
            resp = requests.post(url, timeout=self.to, headers=self.headers, data=body_json)
        except Exception as e:
            panic(e=e, resp=resp)

        if resp.status_code not in codes_allowed:
            panic(resp=resp)
        return resp.json(), resp.headers.get('location')

