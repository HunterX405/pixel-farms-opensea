import httpx
import asyncio

class HunterAPI:

    def __init__(self, http2=True):
        self.client = httpx.AsyncClient(http2=http2)
        self.logging = False
        self.logs = False

    def log_message(self, message):
        if self.logs:
            print(message)
            if not self.logging:
                LINE_UP = '\033[1A'
                LINE_CLEAR = '\x1b[2K'
                print(LINE_UP, end=LINE_CLEAR)

    async def log_request(self, request):
        self.log_message(f"{request.method} {request.url} - Waiting for response")

    async def log_response(self, response):
        request = response.request
        self.log_message(f"{request.method} {request.url} - Status {response.status_code}")

    def set_api_key(self, api_key):
        self.client.headers["X-API-KEY"] = api_key

    async def call(self, req: httpx.Request, retries=0, total_elapsed=0, backoff_factor=1):
        response = await self.client.send(req)

        if response.status_code != 200:
            sleep_time = backoff_factor * (2 ** (retries - 1))
            request = response.request
            self.log_message(
                f"{request.method} {request.url} - {response.status_code}: {response.reason_phrase} | Sleep: {sleep_time}s")
            await asyncio.sleep(sleep_time)
            retry = retries + 1
            elapsed = total_elapsed + response.elapsed.total_seconds()

            return self.call(req, retry, elapsed)
        
        self.log_message(
            f"Request took {response.elapsed.total_seconds() + total_elapsed:.2f} seconds")

        return response

    async def get(self, url, p=None):
        request = self.client.build_request("GET", url, params=p)
        return await self.call(request)

    async def post(self, url, data=None, content=None):
        request = self.client.build_request("POST", url, data=data, content=content)
        response = await self.call(request)
        self.log_message(response.text)
        return response
