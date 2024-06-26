import asyncio
import logging
import typing

import aiohttp
from tenacity import (
    after_log,
    before_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)


class HttpClient:
    def __init__(
        self,
        retry_attempts: int = 3,
        retry_wait: int = 1,
        timeout: int = 10,
        logger: typing.Optional[logging.Logger] = None,
    ):
        self.session = None
        self.retry_attempts = retry_attempts
        self.retry_wait = retry_wait
        self.timeout = timeout
        self.logger = logger

        if logger is not None:
            self.before = before_log(logger, logging.DEBUG)
            self.after = after_log(logger, logging.DEBUG)
        else:
            self.before = self.after = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        self.session = None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type((asyncio.exceptions.TimeoutError,)),
    )
    async def get(
        self, url: str, headers=None, allow_redirects: bool = False
    ) -> aiohttp.ClientResponse:
        if self.session is None:
            raise RuntimeError("Session is closed")

        return await self.session.get(
            url, headers=headers, allow_redirects=allow_redirects
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type((asyncio.exceptions.TimeoutError,)),
    )
    async def post(
        self, url: str, data=None, headers=None, allow_redirects: bool = False
    ) -> aiohttp.ClientResponse:
        if self.session is None:
            raise RuntimeError("Session is closed")

        return await self.session.post(
            url, data=data, headers=headers, allow_redirects=allow_redirects
        )

    async def call_every_n_seconds(
        self,
        method: str,
        url: str,
        condition: typing.Callable[[aiohttp.ClientResponse], bool],
        data: typing.Optional[typing.Dict] = None,
        headers: typing.Optional[typing.Dict] = None,
        n: int = 5,
    ) -> aiohttp.ClientResponse:
        while True:
            if method.lower() == "get":
                response = await self.get(url, headers=headers)
            elif method.lower() == "post":
                response = await self.post(url, data=data, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")

            if await condition(response):
                return response

            await asyncio.sleep(n)
            if await condition(response):
                return response

            await asyncio.sleep(n)
