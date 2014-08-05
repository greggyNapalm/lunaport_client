# -*- encoding: utf-8 -*-

"""
    lunaport_client.v1.ammo
    ~~~~~~~~~~~~~~~~~~~~~~~

    Ammo REST resource.
"""

import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

import requests

from exceptions import panic


class Ammo(object):
    def ammo_get(self, ammo_id):
        """
        Fetch ammo entrie **not ammo file** passing uniq identificator.
        Args:
            ammo_id: int

        Returns:
            dict: Ammo entrie respresentation.

        Throws:
            LunaportClientError
        """
        resp = None
        url = '{}ammo/{}'.format(self.epoint, ammo_id)
        try:
            resp = requests.get(url, timeout=self.to)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            panic(e=e, resp=resp)

    def ammo_post(self, case, descr=None, files=None, data=None):
        """
        Upload file to Lunaport service and
        get new REST resource representation in responce.

        User requests_toolbelt.MultipartEncoder for big files.
        Args:
            data: str, whole file.

        Returns:
            dict: New test entrie respresentation.

        Throws:
            LunaportClientError
        """
        resp = None
        codes_allowed = [201, ]
        url = '{}ammo/'.format(self.epoint)

        kw = {'data': {}}
        if files:
            # in mem file
            kw.update({'files': files})
        elif data:
            # requests_toolbelt.MultipartEncoder, if  file doesn't fetas in mem.
            kw.update({'data': data})
        else:
            raise ValueError('Malformed kw, define one of: `files` or `data`')

        kw['data'].update({
            'case': case,
            'descr': descr
        })

        try:
            resp = requests.post(url, **kw)
        except Exception as e:
            panic(e=e, resp=resp)

        if resp.status_code not in codes_allowed:
            panic(resp=resp)
        return resp.json()
