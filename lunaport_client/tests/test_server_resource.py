#import sys
#sys.path.append('../')

import responses
import requests

#from lunaport_client import LunaportClinetv1
#import lunaport_client as lc
#print lc.__version__
#import .. lunaport_client

#from ..lunaport_client import LunaportClinet
#from lunaport_client import LunaportClinet as lunac
#lunac = lunaport_client.LunaportClinetv1()

from ..lunaport_client.http_client import LunaportClinet

@responses.activate
def test_my_api():
    responses.add(responses.GET, 'http://twitter.com/api/1/foobar',
                  body='{"error": "not found"}', status=404,
                  content_type='application/json')

    resp = requests.get('http://twitter.com/api/1/foobar')

    assert resp.json() == {"error": "not found"}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://twitter.com/api/1/foobar'
    assert responses.calls[0].response.content == '{"error": "not found"}'

@responses.activate
def test_my_XXX():
    responses.add(responses.GET, 'http://twitter.com/api/1/foobar',
                  body='{"error": "not found"}', status=404,
                  content_type='application/json')

    resp = requests.get('http://twitter.com/api/1/foobar')

    assert resp.json() == {"error": "not found"}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://twitter.com/api/1/foobar'
    assert responses.calls[0].response.content == '{"error": "not found"}'

@responses.activate
def test_my_YYY():
    responses.add(responses.GET, 'http://twitter.com/api/1/foobar',
                  body='{"error": "not found"}', status=404,
                  content_type='application/json')

    resp = requests.get('http://twitter.com/api/1/foobar')

    assert resp.json() == {"error": "not found"}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://twitter.com/api/1/foobar'
    assert responses.calls[0].response.content == '{"error": "not found"}'
