from flask import Blueprint, jsonify, request, abort
from common.custom_exceptions import ClientError, ServerError
from common.shortly_logger import logger
import requests, json, os

api = Blueprint('api', __name__)


@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
    """
    Returns
    200 json {
                "url": string,
                "link": string
             }
    400 client error
    500 sever error

    :return:
    """
    providers = {'bitly': bitly_short,
                 'tinyurl': tiny_short}
    request_json = request.get_json()
    provider = request_json.get('provider')
    logger.debug(f'Provider requested"{provider}"')
    url = request_json.get('link')

    if url is None:
        logger.warning('No "url" provided! 400')
        abort(400)

    if provider not in providers:
        alt_provider = providers.popitem()
        provider = alt_provider[0]
        provider_fun = alt_provider[1]
        logger.info(f'Provider does not exist. Will use "{provider}".')
    else:
        provider_fun = providers.pop(provider)

    try:
        response = provider_fun(url)
    except ClientError:
        logger.warning(f'Request to "{provider}" returned with 4xx. Aborting with 400!')
        abort(400)
    except ServerError:
        logger.info(f'Request to "{provider}" returned with a 5xx.')
        alt_provider = providers.popitem()
        provider = alt_provider[0]
        provider_fun = alt_provider[1]
        try:
            response = provider_fun(url)
        except ClientError:
            logger.warning(f'Request to "{provider}" returned with 4xx. Aborting with 400!')
            abort(400)
        except ServerError:
            logger.warning('Aborting with 500!')
            abort(500)

    return jsonify(response)


def bitly_short(url):
    """
        Calls the bitly API to shorten given url
        Raises
        1. ClientError if API status code is 4xx
        2. ServerError if API status code is 5xx

        :param url: string
        :return: dict
        """
    data = {'long_url': url}
    headers = {'Accept': 'application/json',
               'Authorization': os.getenv('BITLY_TOKEN')}
    try:
        logger.info(f'Requesting "bitly" to shorten "{url}".')
        response = requests.post('https://api-ssl.bitly.com/v4/shorten', data=json.dumps(data), headers=headers)
    except Exception:
        logger.error('Request FAILED!!')
        raise ServerError

    # 403 response is returned when the BITLY_TOKEN environment variable is invalid!
    if response.status_code == 403:
        logger.error('INVALID BITLY_TOKEN!')
        raise ServerError

    if 400 <= response.status_code < 500 :
        logger.error('Request responded with 4xx.')
        raise ClientError

    if 500 <= response.status_code < 600 :
        logger.error('Request responded with 5xx.')
        raise ServerError

    resp_json = response.json()
    short_url = resp_json['link']
    return prepare_response(url, short_url)


def tiny_short(url):
    """
    Calls the tinyurl API to shorten given url
    Raises
    1. ClientError if API status code is 4xx
    2. ServerError if API status code is 5xx

    :param url: string
    :return: dict
    """
    try:
        logger.info(f'Requesting "tinyurl" to shorten "{url}".')
        response = requests.get('http://tinyurl.com/api-create.php', params={'url': url})
    except Exception:
        logger.error('Request FAILED!!')
        raise ServerError

    # For now tinyurl seems always to return a 200 response but just for future proofing.
    if 400 <= response.status_code < 500:
        logger.error('Request responded with 4xx.')
        raise ClientError

    if 500 <= response.status_code < 600:
        logger.error('Request responded with 5xx.')
        raise ServerError

    return prepare_response(url, response.content.decode('utf-8'))


def prepare_response(url, short_link):
    """
    Creates a dictionary containing
    1. url requested to be shorten
    2. shortened url

    :param url: string
    :param short_link: string
    :return: dict
    """
    if url is None or short_link is None:
        logger.error('Missing url or short_link.')
        raise ServerError

    return {
        'url': url,
        'link': short_link
    }
