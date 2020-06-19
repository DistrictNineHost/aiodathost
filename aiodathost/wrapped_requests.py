from .resources import SESSIONS, CONFIG
from .exceptions import InvalidAuthorization, UndefinedError, \
    BadRequest, RequestTimeout, InternalError, NotFound, AboveDiskQuota


class AWR:
    headers = {
        "Accept": "application/json",
    }

    def __init__(self, route, **kwargs):
        self.route = route

        self.kwargs = kwargs

    async def _raise_exception(self, resp):
        error_message = await resp.json()

        if "response" in error_message and \
                "error" in error_message["response"]:
            error_message = error_message["response"]["error"]
        else:
            error_message = None

        if resp.status == 401:
            raise InvalidAuthorization(error_message)
        elif resp.status == 404:
            raise NotFound(error_message)
        elif resp.status == 400:
            raise BadRequest(error_message)
        elif resp.status == 408:
            raise RequestTimeout(error_message)
        elif resp.status == 500:
            raise InternalError(error_message)
        elif resp.status == 507:
            raise AboveDiskQuota(error_message)
        else:
            raise UndefinedError(error_message)

    async def get(self, read=False):
        """ Wrapped get request """

        async with SESSIONS.AIOHTTP.get(
            self.route,
            auth=SESSIONS.AUTH,
            headers=self.headers,
                **self.kwargs) as resp:
            if resp.status == 200:
                if not read:
                    return await resp.json()
                else:
                    return await resp.read()
            else:
                await self._raise_exception(resp)

    async def get_stream(self):
        """
        Steam downloads content.
        """

        async with SESSIONS.AIOHTTP.get(
            self.route,
            auth=SESSIONS.AUTH,
            headers=self.headers,
                **self.kwargs) as resp:
            if resp.status == 200:
                chunk = True

                while chunk:
                    chunk = await resp.content.read(CONFIG.chunk_size)

                    if chunk:
                        yield chunk
            else:
                await self._raise_exception(resp)

    async def post(self, json=False):
        """ Wrapped post request """

        async with SESSIONS.AIOHTTP.post(
            self.route,
            auth=SESSIONS.AUTH,
            headers=self.headers,
                **self.kwargs) as resp:
            if resp.status == 200:
                if not json:
                    return True
                else:
                    return await resp.json()
            else:
                await self._raise_exception(resp)

    async def delete(self):
        """ Wrapped delete request """

        async with SESSIONS.AIOHTTP.delete(
            self.route,
            auth=SESSIONS.AUTH,
            headers=self.headers,
                **self.kwargs) as resp:
            if resp.status == 200:
                return True
            else:
                await self._raise_exception(resp)

    async def put(self):
        """ Wrapped put request """

        async with SESSIONS.AIOHTTP.put(
            self.route,
            auth=SESSIONS.AUTH,
            headers=self.headers,
                **self.kwargs) as resp:
            if resp.status == 200:
                return True
            else:
                await self._raise_exception(resp)
