import pytest
from shorty.api import prepare_response
from common.custom_exceptions import ServerError


class TestPrepareResponse:
    def test_valid_input(self):
        output = prepare_response('url', 'link')
        expected = {
            'url': 'url',
            'link': 'link'
        }

        assert output == expected

    def test_none_url(self):
        with pytest.raises(ServerError):
            prepare_response(url=None, short_link='link')

    def test_none_short_link(self):
        with pytest.raises(ServerError):
            prepare_response(url='url', short_link=None)

    def test_both_none(self):
        with pytest.raises(ServerError):
            prepare_response(url=None, short_link=None)

