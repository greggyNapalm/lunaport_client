# -*- encoding: utf-8 -*-

"""
    exceptions for Lunaport client
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    xxx
"""

import pprint
pp = pprint.PrettyPrinter(indent=4)


class LunaportClientError(Exception):
    def __init__(self, msg, url=None, status_code=None, resp_body=None,
                 orig_e=None, resp_obj=None):

        self.orig_e = orig_e
        self.msg = msg
        self.resp_obj = resp_obj
        if resp_obj is None:
            self.url = url
            self.status_code = status_code
            self.resp_body = resp_body
        else:
            self.url = resp_obj.url
            self.status_code = resp_obj.status_code
            self.resp_body = resp_obj.text

            try:
                doc = resp_obj.json()
                self.error_type = doc.get('error_type')
                self.error_text = doc.get('error_text')
            except Exception:
                pass

    def __str__(self):
        msg = [self.msg]
        if self.url:
            msg.append('URL:{}'.format(self.url))
        if self.status_code:
            msg.append('HTTP STATUS CODE:{}'.format(self.status_code))
        if self.resp_body:
            msg.append('RESP BODY:{}'.format(self.resp_body))

        return repr(';'.join(msg))

    def reraise(self):
        params = {
            'url': self.url,
            'status_code': self.status_code,
            'resp_body': self.resp_body,
            'orig_e': self.orig_e,
            'resp_obj': self.resp_obj
        }
        raise LunaportClientError(self.msg, **params)

    @property
    def missing_issue(self):
        if hasattr(self, 'error_text'):
            return 'unknown *issue*' in self.error_text
        return False

    @property
    def missing_user(self):
        tgt_msg = [
            'unknown *user*',
            'unknown *reporter*',
            'unknown *assignee*',
            'unknown *initiator*',
        ]
        if hasattr(self, 'error_text'):
            for msg in tgt_msg:
                if msg in self.error_text:
                    return True
        return False

    @property
    def missing_server(self):
        if hasattr(self, 'error_text'):
            return ('unknown *load_src*' in self.error_text) or (
                'unknown *load_dst*' in self.error_text)
        return False

    @property
    def missing_proj(self):
        if hasattr(self, 'error_text'):
            return 'unknown *project_id*' in self.error_text
        return False

    @property
    def miss_resource(self):
        """ Returns missing resource value.
            error_text format: <some err text:resource_value>
        """
        if hasattr(self, 'error_text'):
            return self.error_text.split(':')[-1].rstrip('\'')
        return False


def panic(e=None, resp=None, text=None):
    msg = ''
    kw = {}

    if text:
        msg += text
    if e:
        msg += str(e)
        kw['orig_e'] = e

    if resp is None:
        raise LunaportClientError(msg, **kw)

    if getattr(resp, 'url', None):
        # hide privat HTTP Basic auth
        scheme_auth, path = resp.url.split('@')
        kw['url'] = scheme_auth.split('_')[0] + '<..>@' + path

    if callable(resp.json):
        try:
            resp_msg = resp.json()
            if 'error_text' in resp_msg:
                msg = resp_msg['error_text'] + ';' + msg

            if 'error_type' in resp_msg:
                msg = resp_msg['error_type'] + ':' + msg
        except ValueError:
            # includes simplejson.decoder.JSONDecodeError
            pass

    raise LunaportClientError(msg, **kw)
