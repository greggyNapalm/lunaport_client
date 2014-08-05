# -*- encoding: utf-8 -*-

"""
    lunaport_client.v1.notification
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Notification(how to notiffy user on some test phase) REST resource.
"""

import json
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

import requests

from exceptions import panic


class Notification(object):
    def notifctn_get(self, case_name):
        resp = None
        url = '{}notifications/'.format(self.epoint)
        params = {
            'case_name': case_name,
        }
        try:
            resp = requests.get(url, timeout=self.to, params=params)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)
