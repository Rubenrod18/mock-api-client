import logging
import os

import httpx

from app.exceptions import ExternalApiError, HttpClientError

logger = logging.getLogger(__name__)


class _BaseJSONPlaceholderProvider:
    def __init__(self):
        self.url = os.getenv('JSONPLACEHOLDER_API')

    @staticmethod
    def make_request(
        method: str,
        url: str,
        headers: dict = None,
        params: dict = None,
        data: dict = None,
        json_data: dict = None,
        files: dict = None,
    ) -> dict:
        headers = headers or {'Content-type': 'application/json; charset=UTF-8'}

        try:
            response = httpx.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json_data,
                files=files,
            )

            if response.status_code not in [httpx.codes.OK, httpx.codes.CREATED]:
                logger.debug(f'Response from {url} - {method} - {response.status_code} - {response.text}')
                raise ExternalApiError()

            logger.info(f'Response from {url} - {method} - {response.status_code}')
            return response.json()
        except httpx.RequestError as exc:
            # HACK: Send notification to Slack or other messaging app
            logger.error(f'An error occurred while requesting {exc.request.url!r}.')
            raise HttpClientError()
        except httpx.HTTPStatusError as exc:
            # HACK: Send notification to Slack or other messaging app
            logger.error(f'Error response {exc.response.status_code} while requesting {exc.request.url!r}.')
            raise ExternalApiError()


class _PostProvider(_BaseJSONPlaceholderProvider):
    def __init__(self):
        super().__init__()
        self.url = f'{self.url}/posts'

    def find_by_id(self, post_id: int) -> dict:
        return self.make_request('GET', f'{self.url}/{post_id}')

    def create(self, payload: dict) -> dict:
        return self.make_request('POST', f'{self.url}', json_data=payload)

    def get(self, params: dict | str | tuple) -> dict:
        return self.make_request('GET', f'{self.url}', params=params)

    def patch(self, post_id: int, payload: dict) -> dict:
        return self.make_request('PATCH', f'{self.url}/{post_id}', json_data=payload)

    def delete(self, post_id: int) -> dict:
        return self.make_request('DELETE', f'{self.url}/{post_id}')


class JSONPlaceholderProvider:
    def __init__(self):
        self.post = _PostProvider()
