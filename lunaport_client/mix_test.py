# -*- encoding: utf-8 -*-

"""
    lunaport_client.v1.test
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Test REST resource.
"""

import json
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

import requests

from exceptions import panic


class Test(object):
    def test_get(self, test_id):
        """
        Fetch test entrie passing uniq identificator.
        Args:
            test_id: int

        Returns:
            dict: Test entrie respresentation.

        Throws:
            LunaportClientError
        """
        resp = None
        url = '{}tests/{}'.format(self.epoint, test_id)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def test_post_arts(self, load_cfg_path, phout_path, meta=None):
        """
        Create new load test entrie.
        Reduce artefacts to get statistics and metadata.
        Args:
            load_cfg_path: str
            phout_path: str
            meta: dict, test entrie metadata.

        Returns:
            dict: New test entrie respresentation.

        Throws:
            LunaportClientError
        """
        resp = None
        codes_allowed = [201, ]
        url = '{}tests/'.format(self.epoint)
        files = {
            'load_cfg': load_cfg_path,
            'phout': phout_path,
        }
        try:
            resp = requests.post(url, data=meta, files=files)
        except Exception as e:
            panic(e=e, resp=resp)

        if resp.status_code not in codes_allowed:
            panic(resp=resp)
        return resp.json()

    def test_post_api(self, load_cfg):
        """
        Create new load test entrie. Launch new test using load_cfg.
        Args:
            load_cfg: dict, ynadex.tank + lunaport section.

        Returns:
            dict: New test entrie respresentation.

        Throws:
            LunaportClientError
        """
        resp = None
        codes_allowed = [201, ]
        url = '{}tests/?force=true'.format(self.epoint)
        try:
            resp = requests.post(url, data=json.dumps(load_cfg),
                                 headers={'Content-type': 'application/json'})
        except Exception as e:
            panic(e=e, resp=resp)

        if resp.status_code not in codes_allowed:
            panic(resp=resp)
        return resp.json()

    def test_patch(self, test_id, diff):
        """
        Patch existing test entrie.
        Args:
            test_id: int
            diff: dict

        Returns:
            dict: New test entrie respresentation.

        Throws:
            LunaportClientError
        """
        resp = None
        url = '{}tests/{}'.format(self.epoint, test_id)
        try:
            resp = requests.patch(url, data=json.dumps(diff), headers=self.headers)
            resp.raise_for_status()
            return resp.json(), resp.headers.get('location')
        except Exception as e:
            panic(e=e, resp=resp)
