import sys
sys.path.append('../')

import responses
import requests

#import lunaport_client

#from ..lunaport_client import LunaportClinet
#from lunaport_client import LunaportClinet as lunac

@responses.activate
def test_issue_api():
    responses.add(responses.GET, 'http://twitter.com/api/1/foobar',
                  body='{"error": "not found"}', status=404,
                  content_type='application/json')

    resp = requests.get('http://twitter.com/api/1/foobar')

    assert resp.json() == {"error": "not found"}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://twitter.com/api/1/foobar'
    assert responses.calls[0].response.content == '{"error": "not found"}'

@responses.activate
def test_issue_XXX():
    responses.add(responses.GET, 'http://twitter.com/api/1/foobar',
                  body='{"error": "not found"}', status=404,
                  content_type='application/json')

    resp = requests.get('http://twitter.com/api/1/foobar')

    assert resp.json() == {"error": "not found"}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://twitter.com/api/1/foobar'
    assert responses.calls[0].response.content == '{"error": "not found"}'

@responses.activate
def test_issue_YYY():
    responses.add(responses.GET, 'http://twitter.com/api/1/foobar',
                  body='{"error": "not found"}', status=404,
                  content_type='application/json')

    resp = requests.get('http://twitter.com/api/1/foobar')

    assert resp.json() == {"error": "not found"}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://twitter.com/api/1/foobar'
    assert responses.calls[0].response.content == '{"error": "not found"}'
