import json, os


bitly_response = {
    "link": "http://bit.ly/2DnlW2V",
    "url": "http://www.wikipedia.com"
}

tinyurl_response = {
    "link": "http://tinyurl.com/bk34e",
    "url": "http://www.wikipedia.com"
}

response_400 = {
    "error": "Client error"
}

response_500 = {
    "error": "Server error"
}

valid_responses = (bitly_response, tinyurl_response,)


class TestRoute:
    def test_provider_link_present_tinyurl_200(self, client):
        data = {
            'provider': 'tinyurl',
            'link': 'http://www.wikipedia.com'
        }
        rv = client.post('/shortlinks',
                           data=json.dumps(data),
                           content_type='application/json')
        assert rv.status == '200 OK'
        assert json.loads(rv.data) == tinyurl_response

    def test_provider_link_present_bitly_200(self, client):
        data = {
            'provider': 'bitly',
            'link': 'http://www.wikipedia.com'
        }
        rv = client.post('/shortlinks',
                           data=json.dumps(data),
                           content_type='application/json')
        assert rv.status == '200 OK'
        assert json.loads(rv.data) == bitly_response

    def test_invalid_provider_200(self, client):
        data = {
            'provider': 'invalid',
            'link': 'http://www.wikipedia.com'
        }
        rv = client.post('/shortlinks',
                           data=json.dumps(data),
                           content_type='application/json')
        assert rv.status == '200 OK'
        assert json.loads(rv.data) in valid_responses

    def test_no_provider_present_200(self, client):
        data = {
            'link': 'http://www.wikipedia.com'
        }
        rv = client.post('/shortlinks',
                           data=json.dumps(data),
                           content_type='application/json')
        assert rv.status == '200 OK'
        assert json.loads(rv.data) in valid_responses

    def test_no_link_present_400(self, client):
        data = {
            'provider': 'tinyurl',
        }
        rv = client.post('/shortlinks',
                           data=json.dumps(data),
                           content_type='application/json')
        assert rv.status_code == 400
        assert json.loads(rv.data) == response_400

    def test_invalid_link_bitly_400(self, client):
        data = {
            'link': 'invalid',
            'provider': 'bitly'
        }
        rv = client.post('/shortlinks',
                           data=json.dumps(data),
                           content_type='application/json')
        assert rv.status_code == 400
        assert json.loads(rv.data) == response_400


