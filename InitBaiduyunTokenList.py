import logging, requests

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def get_access_token_str(api_key, secret_key):
    token_request_url = 'https://aip.baidubce.com/oauth/2.0/token'
    token_request_params = dict(grant_type='client_credentials', client_id=api_key, client_secret=secret_key)
    token_request = requests.get(url=token_request_url, params=token_request_params)
    open('baiduyun_access_token.json', 'a').write(token_request.text)


get_access_token_str(api_key='VcI6kj211iHVwbSkCcUctPaK', secret_key='ewTduLnYpTbfKs5ZdvqEDDaCTBBjhwum')
