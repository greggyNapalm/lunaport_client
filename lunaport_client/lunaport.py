# -*- encoding: utf-8 -*-

"""
    lunaport_client
    ~~~~~~~~~~~~~~~

    REST API Client library for Lunaport API.
    @see API docs:
    FIXME: docs lnk here
"""

import socket
from functools import wraps
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

import requests
from requests import Request, Session
from requests.auth import HTTPBasicAuth

from . import __version__
from exceptions import LunaportClientError


class LunaportClinet(object):
    """HTTP client for both APIs: KSHM and Tank.

        Attributes:
            base: str, base uri for querying.
            to: float, HTTP request time out.
    """
    __version__ = __version__
    _endpoint_tmpl = 'http://{}/api/v1.0/'

    def __init__(self, fqdn='lunaport.domain.ru',
                 endpoint_tmpl=None, to=10.0, test_id=None, auth=None):
        self.to = to
        self.fqdn = fqdn
        self.test_id = test_id
        self.endpoint_tmpl = endpoint_tmpl or self._endpoint_tmpl
        assert isinstance(auth, (list, tuple)), 'Wrong *auth* param type.'
        self.auth = HTTPBasicAuth(*auth)
        self.s = Session()

    def compose_endpoint(f):
        """ Check the required parameters, generate API endpoint addr
            like http://api.host.org/api/v2.1
            First f positional argument shud be class instance(aka self),
            so don't use this decorator with static methods.
        Args:
            f - function obj to wrap.

        Returns:
            f - original func with modified params: *to*, *endpoint*
        """
        @wraps(f)
        def decorated(*args, **kw):
            self = args[0]

            to = kw.get('to', None) or self.to
            assert to, '*to* - Time out parameter missing'
            fqdn = kw.get('fqdn', None) or self.fqdn
            assert fqdn, '*fqdn* - domain name parameter missing'
            endpoint_tmpl = kw.get('endpoint_tmpl', None) or self.endpoint_tmpl
            assert endpoint_tmpl, '*endpoint_tmpl* parameter missing'

            kw.update({
                'endpoint': endpoint_tmpl.format(fqdn),
                'to': to,
                #'auth': self.auth,
            })

            if kw.get('fqdn', None):
                del kw['fqdn']  # no more needed. use endpoint param.
            return f(*args, **kw)

        return decorated

    def _http_call(self, r, **kw):
        """ Send HTTP request to remote side, handle common errors(TCP and HTTP
            timeouts, wrongs status codes and deserialization).
            for more info @see:
            http://www.python-requests.org/en/latest/api/#requests.Response

        Args:
            r - request object.
            to - float, imeout awaiting http response in seconds.
            codes_allowed - list of int.
            ret_obj - bool, if True, return responce obj without status code
                checks and JSON deserialization.
        Returns:
            dict or responce object.
        """
        try:
            #resp = self.s.send(r, **kw)
            resp = self.s.send(r, timeout=kw.get('to', None))
        except requests.exceptions.ConnectionError, e:
            raise LunaportClientError(
                'Can\'t connect to API host @see orig_e attr for details.',
                url=r.url, orig_e=e)
        except socket.error, e:
            raise LunaportClientError(str(e), url=r.url, orig_e=e)
        except requests.exceptions.Timeout, e:
            raise LunaportClientError(str(e), url=r.url, orig_e=e)

        if kw.get('ret_obj', None):  # return resp without any validations
            return resp

        codes_allowed = kw.get('codes_allowed', None) or [200, ]
        if not resp.status_code in codes_allowed:
            msg = [
                'Wrong HTTP response status code:{}'.format(resp.status_code),
                'acceptable codes list: {}'.format([c for c in codes_allowed])
            ]
            raise LunaportClientError(' '.join(msg), resp_obj=resp)
        return resp

    @compose_endpoint
    def tests(self, to=None, endpoint=None, codes_allowed=[200, ],
              ret_obj=False, **kw):
        """ Retrieve  tank(load generation server) status.
        Args:
            to - float, timeout awaiting http response in seconds.
            endpoint - str, API base url.
            codes_allowed - list of int.
            ret_obj - bool.

        Returns:
            resp - responce object.
        """
        assert all([to, endpoint])
        url = '{}tests'.format(endpoint)
        return self._http_call(Request('GET', url,  auth=self.auth).prepare(),
                               to=to, codes_allowed=codes_allowed,
                               ret_obj=ret_obj)

    @compose_endpoint
    def create_t_from_arts(self, meta, load_cfg_path, phout_path, to=None,
                           endpoint=None, codes_allowed=[201, ],
                           ret_obj=False, **kw):
        """ Create new test resource from artifacts(load.cfg, phout).
        Shud be used with tests luanched in console with Yandex-tank.
        Args:
            meta - dict, required test metadata(case, initiatior, env, etc).
            load_cfg_path - fileobj, test config(load.cfg - Yandex tank formt).
            phout - fileobj, test result statistic file(Phout format).
            to - float, timeout awaiting http response in seconds.
            endpoint - str, API base url.
            codes_allowed - list of int.
            ret_obj - bool.

        Returns:
            tuple(resource location, resource repr)
            or
            resp - responce object.
        """
        assert all([to, endpoint])
        assert isinstance(meta, dict), 'Wrong *meta* param type, dict required'
        url = '{}tests/'.format(endpoint)
        files = {
            'load_cfg': load_cfg_path,
            'phout': phout_path,
        }
        req = Request('POST', url, data=meta, files=files,
                      auth=self.auth).prepare()

        rv = self._http_call(req, to=to, codes_allowed=codes_allowed,
                             ret_obj=True)
        if ret_obj:
            return rv

        return rv.headers.get('location'), rv.json()

    @compose_endpoint
    def create_t_lunapark(self, t_test_id, t_fqdn, lunapark_id, to=None,
                          endpoint=None, codes_allowed=[201, ], ret_obj=False,
                          retries_num=5, **kw):
        """ Create new test resource.
        Shud be used with tests luanched via tank API.
        Args:
            t_test_id - int, Tank test id.
            t_fqdn - str, Tank fqdn.
            lunapark_id - int, Lunapark test id.
            to - float, timeout awaiting http response in seconds.
            endpoint - str, API base url.
            codes_allowed - list of int.
            ret_obj - bool.
            tyres_num - int, recursive calls counter.

        Returns:
            tuple(resource location, resource repr)
            or
            resp - responce object.
        """
        if retries_num <= 0:
            msg = [
                'Something goes wrong,'
                'max method calls retries exceeded'
            ]
            raise LunaportClientError(' '.join(msg))

        assert all([to, endpoint])
        url = '{}tests/'.format(endpoint)
        headers = {'Content-type': 'application/json'}
        body = {
            'case': kw['case'],
            'initiator': kw['initiator'],
            'env': 'luna-tank-api',
            't_tank_id': t_test_id,
            'tank_fqdn': t_fqdn,
            'luna_id': lunapark_id,
            'autocomplete': kw.get('autocomplete', False),
        }
        body_json = json.dumps(body)
        req = Request('POST', url, data=body_json, headers=headers,
                      auth=self.auth).prepare()

        try:
            rv = self._http_call(req, to=to, codes_allowed=codes_allowed,
                                 ret_obj=ret_obj)
        except LunaportClientError as e:
            # TODO: remove missing resource handling on client side.
            # Moved to reevice side allready.
            if e.missing_issue:
                print 'auto creating missing issue:{}'.format(e.miss_resource)
                self.create_issue(e.miss_resource, to=to, endpoint=endpoint,
                                  ret_obj=False)
            elif e.missing_server:
                print 'auto creating missing server:{}'.format(e.miss_resource)
                self.create_server(e.miss_resource, to=to, endpoint=endpoint,
                                   ret_obj=False)
            else:
                e.reraise()

            retries_num -= 1
            return self.create_t_lunapark(
                t_test_id, t_fqdn, lunapark_id, to=to, endpoint=endpoint,
                ret_obj=ret_obj, codes_allowed=codes_allowed,
                retries_num=retries_num, **kw)

        return rv.headers.get('location'), rv.json()

    @compose_endpoint
    def create_issue(self, issue_name, to=None, endpoint=None,
                     codes_allowed=[201, ], ret_obj=False, retries_num=5,
                     **kw):
        """ Create new issue resource.
        Args:
            issue_name - str case insensitive, like SOMEPROJ-123
            to - float, timeout awaiting http response in seconds.
            endpoint - str, API base url.
            codes_allowed - list of int.
            ret_obj - bool.
            retries_num - int, recursive calls counter.

        Returns:
            tuple(resource location, resource repr)
            or
            resp - responce object.
        """
        if retries_num <= 0:
            msg = [
                'Something goes wrong,'
                'max method calls retries exceeded'
            ]
            raise LunaportClientError(' '.join(msg))

        assert all([to, endpoint])
        url = '{}issue/'.format(endpoint)
        headers = {'Content-type': 'application/json'}
        body = {
            'name': issue_name,
        }
        body_json = json.dumps(body)
        req = Request('POST', url, data=body_json, headers=headers,
                      auth=self.auth).prepare()

        try:
            rv = self._http_call(req, to=to, codes_allowed=codes_allowed,
                                 ret_obj=ret_obj)
        except LunaportClientError as e:
            if e.missing_user:
                print 'auto creating missing user:{}'.format(e.miss_resource)
                self.create_user(e.miss_resource, to=to, endpoint=endpoint,
                                 ret_obj=False)
            else:
                e.reraise()

            retries_num -= 1
            return self.create_issue(issue_name, to=to,
                                     endpoint=endpoint, ret_obj=ret_obj,
                                     codes_allowed=codes_allowed,
                                     retries_num=retries_num, **kw)

        return rv.headers.get('location'), rv.json()

    @compose_endpoint
    def create_server(self, fqdn=None, ip_addr=None, to=None, endpoint=None,
                      codes_allowed=[201, ], ret_obj=False, **kw):
        """ Create new server resource.
        Args:
            fqdn - str, fully qualified domain name.
            ip_addr - str, ipv4 addr.
            to - float, timeout awaiting http response in seconds.
            endpoint - str, API base url.
            codes_allowed - list of int.
            ret_obj - bool.
            retries_num - int, recursive calls counter.

        Returns:
            tuple(resource location, resource repr)
            or
            resp - responce object.
        """
        assert all([to, endpoint])
        url = '{}host/'.format(endpoint)
        headers = {'Content-type': 'application/json'}
        body = {
            'fqdn': fqdn,
        }
        body_json = json.dumps(body)
        req = Request('POST', url, data=body_json, headers=headers,
                      auth=self.auth).prepare()

        rv = self._http_call(req, to=to, codes_allowed=codes_allowed,
                             ret_obj=ret_obj)
        return rv.headers.get('location'), rv.json()

    @compose_endpoint
    def create_user(self, login, to=None, endpoint=None,
                    codes_allowed=[201, ], ret_obj=False, **kw):
        """ Create new user resource.
        Args:
            login - str, user login attr.
            to - float, timeout awaiting http response in seconds.
            endpoint - str, API base url.
            codes_allowed - list of int.
            ret_obj - bool.
            retries_num - int, recursive calls counter.

        Returns:
            tuple(resource location, resource repr)
            or
            resp - responce object.
        """
        assert all([to, endpoint])
        url = '{}user/'.format(endpoint)
        headers = {'Content-type': 'application/json'}
        body = {
            'login': login,
        }
        body_json = json.dumps(body)
        req = Request('POST', url, data=body_json, headers=headers,
                      auth=self.auth).prepare()

        rv = self._http_call(req, to=to, codes_allowed=codes_allowed,
                             ret_obj=ret_obj)
        return rv.headers.get('location'), rv.json()

    @compose_endpoint
    def update_test(self, diff, test_id, to=None, endpoint=None,
                     codes_allowed=[200, ], ret_obj=False, **kw):
        """ Partially update test resource.
        Args:
            diff - dict, dict of attr-value pairs to update.
            test_id - int, Lunaport test id.
            to - float, timeout awaiting http response in seconds.
            endpoint - str, API base url.
            codes_allowed - list of int.
            ret_obj - bool.

        Returns:
            tuple(resource location, resource repr)
            or
            resp - responce object.
        """
        assert all([to, endpoint])
        url = '{}tests/{}'.format(endpoint, test_id)
        hdrs = {'Content-type': 'application/json'}
        req = Request('PATCH', url, data=json.dumps(diff), headers=hdrs,
                      auth=self.auth).prepare()
        rv = self._http_call(req, to=to, codes_allowed=codes_allowed,
                             ret_obj=ret_obj)
        if ret_obj:
            return rv
        return rv.headers.get('location'), rv.json()

    @compose_endpoint
    def create_stat(self, test_id, ammo_tag, ver, doc, to=None, endpoint=None,
                    codes_allowed=[201, ], ret_obj=False, **kw):
        """ Create new stat resource.
        Args:
            test_id - int, Lunaport test uniq id.
            ver - str, stat struct version like '0.5.4'
            doc - dict, statistic document to send.
            to - float, timeout awaiting http response in seconds.
            endpoint - str, API base url.
            codes_allowed - list of int.
            ret_obj - bool.
            retries_num - int, recursive calls counter.

        Returns:
            dcit - resource repr
            or
            resp - responce object.
        """
        assert all([to, endpoint])
        url = '{}tests/{}/stat/{}'.format(endpoint, test_id, ammo_tag)
        headers = {'Content-type': 'application/json'}
        body_json = json.dumps({
            'version': ver,
            'doc': doc,
        })
        req = Request('POST', url, data=body_json, headers=headers,
                      auth=self.auth).prepare()

        rv = self._http_call(req, to=to, codes_allowed=codes_allowed,
                             ret_obj=ret_obj)
        return rv.json()

    @compose_endpoint
    def create_chart(self, test_id, ammo_tag, ver, doc, to=None, endpoint=None,
                    codes_allowed=[201, ], ret_obj=False, **kw):
        """ Create new chart resource.
        Args:
            test_id - int, Lunaport test uniq id.
            ver - str, stat struct version like '0.5.4'
            doc - dict, statistic document to send.
            to - float, timeout awaiting http response in seconds.
            endpoint - str, API base url.
            codes_allowed - list of int.
            ret_obj - bool.
            retries_num - int, recursive calls counter.

        Returns:
            dcit - resource repr
            or
            resp - responce object.
        """
        assert all([to, endpoint])
        url = '{}tests/{}/chart/{}'.format(endpoint, test_id, ammo_tag)
        headers = {'Content-type': 'application/json'}
        body_json = json.dumps({
            'version': ver,
            'doc': doc,
        })
        req = Request('POST', url, data=body_json, headers=headers,
                      auth=self.auth).prepare()

        rv = self._http_call(req, to=to, codes_allowed=codes_allowed,
                             ret_obj=ret_obj)
        return rv.json()

    @compose_endpoint
    def create_eval(self, test_id, oracle, result, passed, to=None,
                    endpoint=None, codes_allowed=[201, ], ret_obj=False,
                    **kw):
        """ 
        Create new test evaluation resource.
        Args:
            test_id - int, Lunaport test uniq id.
            oracle - dict.
            result - dict, asserts execution result.
            passed- Bool, True if test passed well.
            to - float, timeout awaiting http response in seconds.
            endpoint - str, API base url.
            codes_allowed - list of int.
            ret_obj - bool.
            retries_num - int, recursive calls counter.

        Returns:
            tuple(resource location, resource repr)
            or
            resp - responce object.
        """
        assert all([to, endpoint])
        url = '{}eval/'.format(endpoint)
        #'http://lunaport.domain.ru/api/v1.0/eval/'
        headers = {'Content-type': 'application/json'}
        body_json = json.dumps({
            'test_id': test_id,
            'oracle': oracle,
            'result': result,
            'passed': passed,
        })
        req = Request('POST', url, data=body_json, headers=headers,
                      auth=self.auth).prepare()

        rv = self._http_call(req, to=to, codes_allowed=codes_allowed,
                             ret_obj=ret_obj)
        if ret_obj:
            return rv

        return rv.headers.get('location'), rv.json()

    @compose_endpoint
    def create_proj(self, proj_name, to=None, endpoint=None,
                    codes_allowed=[201, ], ret_obj=False, **kw):
        """ Create new user resource.
        Args:
            proj_name - str, KEY in Jira/Startrack domain.
            to - float, timeout awaiting http response in seconds.
            endpoint - str, API base url.
            codes_allowed - list of int.
            ret_obj - bool.
            retries_num - int, recursive calls counter.

        Returns:
            tuple(resource location, resource repr)
            or
            resp - responce object.
        """
        assert all([to, endpoint])
        url = '{}proj/'.format(endpoint)
        headers = {'Content-type': 'application/json'}
        body = {
            'name': proj_name,
        }
        body_json = json.dumps(body)
        req = Request('POST', url, data=body_json, headers=headers,
                      auth=self.auth).prepare()

        rv = self._http_call(req, to=to, codes_allowed=codes_allowed,
                             ret_obj=ret_obj)
        return rv.headers.get('location'), rv.json()

    @compose_endpoint
    def get_case(self, case_id, to=None, endpoint=None, codes_allowed=[200, ],
                 ret_obj=False, **kw):
        """
        Fetch case resource located by id.
        Args:
            case_id - int, case uniq id.
            to - float, timeout awaiting http response in seconds.
            endpoint - str, API base url.
            codes_allowed - list of int.
            ret_obj - bool.
            retries_num - int, recursive calls counter.

        Returns:
            tuple(resource location, resource repr)
            or
            resp - responce object.
        """
        assert all([to, endpoint])
        url = '{}case/{}'.format(endpoint, case_id)
        headers = {'Content-type': 'application/json'}
        req = Request('GET', url, headers=headers, auth=self.auth).prepare()

        rv = self._http_call(req, to=to, codes_allowed=codes_allowed,
                             ret_obj=ret_obj)
        if ret_obj:
            return rv

        return rv.headers.get('location'), rv.json()

    @compose_endpoint
    def get_notifications(self, case_name, to=None, endpoint=None,
                          codes_allowed=[200, ], ret_obj=False, **kw):
        assert all([to, endpoint])
        # http://dev.lunaport.domain.ru/api/v1.0/notifications/?case_name=usr-gkomissarov-dev
        url = '{}notifications/'.format(endpoint)
        params = {
            'case_name': case_name,
        }
        headers = {'Content-type': 'application/json'}
        req = Request('GET', url, params=params, headers=headers, auth=self.auth).prepare()

        rv = self._http_call(req, to=to, codes_allowed=codes_allowed,
                             ret_obj=ret_obj)
        if ret_obj:
            return rv

        return rv.json()

    @compose_endpoint
    def get_issue(self, issue_name, to=None, endpoint=None,
                  codes_allowed=[200, ], ret_obj=False, **kw):
        assert all([to, endpoint])
        url = '{}issue/{}'.format(endpoint, issue_name)
        req = Request('GET', url, auth=self.auth).prepare()

        rv = self._http_call(req, to=to, codes_allowed=codes_allowed,
                             ret_obj=ret_obj)
        if ret_obj:
            return rv

        return rv.json()
    @compose_endpoint

    def get_test(self, test_id, to=None, endpoint=None,
                  codes_allowed=[200, ], ret_obj=False, **kw):
        assert all([to, endpoint])
        url = '{}tests/{}'.format(endpoint, test_id)
        req = Request('GET', url, auth=self.auth).prepare()

        rv = self._http_call(req, to=to, codes_allowed=codes_allowed,
                             ret_obj=ret_obj)
        if ret_obj:
            return rv

        return rv.json()
