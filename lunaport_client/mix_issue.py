# -*- encoding: utf-8 -*-

"""
    lunaport_client.v1.issue
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Issue(copied from issue tracker entrie) REST resource.
"""

import json
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

import requests

from exceptions import panic


class Issue(object):
    def issue_get(self, issue_name):
        resp = None
        url = '{}issue/{}'.format(self.epoint, issue_name)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def issue_get_names_butch(self):
        resp = None
        url = '{}issue/?names_butch=true'.format(self.epoint)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def issue_post(self, issue_name):
        """ All meta data will be fetched from issue tracker if possible.
        """
        resp = None
        codes_allowed = [201, ]
        url = '{}issue/'.format(self.epoint)
        body_json = json.dumps({
            'name': issue_name,
        })
        try:
            resp = requests.post(url, timeout=self.to, headers=self.headers, data=body_json)
        except Exception as e:
            panic(e=e, resp=resp)

        if resp.status_code not in codes_allowed:
            panic(resp=resp)
        return resp.json(), resp.headers.get('location')
