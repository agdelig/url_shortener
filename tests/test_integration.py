import os, pytest
from shorty import api
from common.custom_exceptions import ServerError, ClientError
from tests.test_route import bitly_response, tinyurl_response


class TestIntegration:
    def test_tinyurl_valid_url(self):
        assert api.tiny_short('http://www.wikipedia.com') == tinyurl_response

    def test_bitly_valid_url(self):
        assert api.bitly_short('http://www.wikipedia.com') == bitly_response

    def test_bitly_invalid_token_raises_ServerError(self):
        token_env_name = 'BITLY_TOKEN'
        token = os.getenv(token_env_name)
        os.environ[token_env_name] = 'invalid'  # Change env var to make bitly respond with a 403

        with pytest.raises(ServerError):
            api.bitly_short('http://www.wikipedia.com')

        os.environ[token_env_name] = token  # Revert env var to correct value

    def test_bitly_invalid_url_raises_ClientError(self):
        with pytest.raises(ClientError):
            api.bitly_short('invalid_url')

