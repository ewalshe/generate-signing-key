#!/usr/bin/env python3

import argparse
import json
import logging
import requests
import uuid


class ApiError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


def process(api_key, size):
    params = {
        'apiKey': api_key,
        'n': 1, 'size': size,
        'format': 'hex'
    }
    payload = {
        'jsonrpc': '2.0', 'method': 'generateBlobs',
        'params': params, 'id': uuid.uuid4().hex
    }
    r = requests.post('https://api.random.org/json-rpc/2/invoke', json=payload)
    if r.status_code != requests.codes.ok:
        raise ApiError(f'Request to random.org failed: {r.text}', status_code=r.status_code)
    response = r.json()
    if 'error' in response:
        raise ApiError(f"Request to random.org failed: {response['error']['message']}", status_code=r.status_code)

    return response['result']['random']['data'][0]


def main(args):
    key_size = int(args.key_size)
    if key_size % 8 != 0:
        raise ValueError(f'Number of bits requested must be a multiple of 8')

    with open(args.credentials_file, 'r') as cf:
        credentials = json.load(cf)

    result = process(credentials['api_key'], key_size)
    print(f"_SIGNING_KEY_{key_size} = '{result}'")


if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s')
    try:
        parser = argparse.ArgumentParser(description='Equus test client')
        parser.add_argument("--credentials-file", "-c", default="api-credentials.json")
        parser.add_argument("--key-size", "-s", default='512')
        arguments = parser.parse_args()
        main(arguments)
    except Exception as exc:
        logging.fatal("App initialisation or critical failure", exc_info=exc)
