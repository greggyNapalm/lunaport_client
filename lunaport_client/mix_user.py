# -*- encoding: utf-8 -*-

"""
    lunaport_client.v1.user
    ~~~~~~~~~~~~~~~~~~~~~~~

    User REST resource.
"""

import json
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

import requests

from exceptions import panic


class User(object):
    def user_get(self, login):
        resp = None
        url = '{}user/{}'.format(self.epoint, login)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def user_get_names_butch(self):
        resp = None
        url = '{}user/?names_butch=true'.format(self.epoint)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)
