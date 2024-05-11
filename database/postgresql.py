import logging
from time import sleep

import requests
from requests.exceptions import RequestException

logger = logging.getLogger("weibo")

def send_post_request_with_token(url, data, token, max_retries, backoff_factor):
    headers = {
        'Content-Type': 'application/json',
        'api-token': f'{token}',
    }
    for attempt in range(max_retries + 1):
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == requests.codes.ok:
                return response.json()
            else:
                raise RequestException(f"Unexpected response status: {response.status_code}")
        except RequestException as e:
            if attempt < max_retries:
                sleep(backoff_factor * (attempt + 1))  # 逐步增加等待时间，避免频繁重试
                continue
            else:
                logger.error(f"在尝试{max_retries}次发出POST连接后，请求失败：{e}")
