# -*- encoding: utf-8 -*-

"""
    lunaport_client.v1.eval
    ~~~~~~~~~~~~~~~~~~~~~~~

    Eval(test result evaluation) REST resource.
"""

import json
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

import requests

from exceptions import panic


class Eval(object):
    def eval_get(self, eval_id):
        resp = None
        url = '{}eval/{}'.format(self.epoint, eval_id)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def eval_post(self, test_id, oracle, result, passed):
        """ Create new test evaluation resource.
        Args:
            test_id - int, Lunaport test uniq id.
            oracle - dict, result validation rules.
            result - dict, asserts execution result.
            passed - Bool, True if test passed well.

        Returns:
            evaluation as dict, location as str.
        """
        resp = None
        codes_allowed = [201, ]
        url = '{}eval/'.format(self.epoint)
        body_json = json.dumps({
            'test_id': test_id,
            'oracle': oracle,
            'result': result,
            'passed': passed,
        })
        try:
            resp = requests.post(url, timeout=self.to, headers=self.headers, data=body_json)
        except Exception as e:
            panic(e=e, resp=resp)

        if resp.status_code not in codes_allowed:
            panic(resp=resp)
        return resp.json(), resp.headers.get('location')
