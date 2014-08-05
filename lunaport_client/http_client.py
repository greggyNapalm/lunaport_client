# -*- encoding: utf-8 -*-
"""
    lunaport_client.http_v2
    ~~~~~~~~~~~~~~~~~~~~~~~

    HTTP based Lunaport service client *second version*.
"""

import os
import pprint
pp = pprint.PrettyPrinter(indent=4)

from . import __version__
from mix_server import Server
from mix_test import Test
from mix_case import Case
from mix_proj import Proj
from mix_issue import Issue
from mix_stat import Stat
from mix_eval import Eval
from mix_dc import Dc
from mix_line import Line
from mix_user import User
from mix_notification import Notification
from mix_ammo import Ammo


ENV_EPOINT = 'LUNAPORT_EPOINT'
ENV_AUTH = 'LUNAPORT_AUTH'


class LunaportClinetBase(object):
    """HTTP client for both APIs: KSHM and Tank.

        Attributes:
            epoint: str, 'http://<PUBLIC_KEY>:<SECRET_KEY>@lunaport.domain.ru'.
            auth: str, '<PUBLIC_KEY>:<SECRET_KEY>'
            to: float, HTTP request time out.
    """
    __version__ = __version__
    _base_path = 'api/v1.0/'
    _default_host = 'lunaport.domain.ru'
    _epoint_tmpl = 'http://{pub}:{prvt}@{host}/' + _base_path

    def __init__(self, epoint=None, auth=None, to=10.0):
        epoint = epoint or os.environ.get(ENV_EPOINT)
        auth = auth or os.environ.get(ENV_AUTH)

        if epoint:
            self.epoint = '{}/{}'.format(epoint, self._base_path)
        elif auth:
            assert isinstance(auth, (basestring, unicode)),\
                'Wrong *auth* param type. Use str("public:secret")'
            public, secret = auth.split(':')
            self.epoint = self._epoint_tmpl.format(**{
                'pub': public,
                'prvt': secret,
                'host': self._default_host
            })
        else:
            raise ValueError('You shude provide: epoint or auth')
        self.to = to
        self.headers = {'Content-type': 'application/json'}

    @staticmethod
    def fillter_dct(keys_allowed, src_dict):
        return {k:src_dict[k] for k in src_dict.keys() if k in keys_allowed}


class LunaportClinetV1(LunaportClinetBase, Server, Test, Case, Proj, Issue, Stat,
                       Eval, Notification, Dc, Line, User, Ammo):
    __just_inherit = True
