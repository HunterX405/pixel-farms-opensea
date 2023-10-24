import httpx
import asyncio


class HunterAPI:

    client = httpx.AsyncClient(http2=True)
    logging = False
    logs = False

    def log_message(message):
        if HunterAPI.logs:
            print(message)
            if not HunterAPI.logging:
                LINE_UP = '\033[1A'
                LINE_CLEAR = '\x1b[2K'
                print(LINE_UP, end=LINE_CLEAR)

    async def log_request(request):
        HunterAPI.log_message(
            f"{request.method} {request.url} - Waiting for response")

    async def log_response(response):
        request = response.request
        HunterAPI.log_message(
            f"{request.method} {request.url} - Status {response.status_code}")

    client.event_hooks['request'] = [log_request]
    client.event_hooks['response'] = [log_response]

    async def call(req: httpx.Request, retries=0, total_elapsed=0, backoff_factor=1):
        response = await HunterAPI.client.send(req)

        if response.status_code != 200:
            sleep_time = backoff_factor * (2 ** (retries - 1))
            request = response.request
            HunterAPI.log_message(
                f"{request.method} {request.url} - {response.status_code}: {response.reason_phrase} | Sleep: {sleep_time}s")
            await asyncio.sleep(sleep_time)
            retry = retries + 1
            elapsed = total_elapsed + response.elapsed.total_seconds()

            return HunterAPI.call(req, retry, elapsed)

        HunterAPI.log_message(
            f"Request took {response.elapsed.total_seconds() + total_elapsed:.2f} seconds")

        return response

    async def get(url, p=None):
        request = HunterAPI.client.build_request("GET", url, params=p)

        return await HunterAPI.call(request)

    async def post(url, data=None, content=None):
        request = HunterAPI.client.build_request("POST", url, data=data, content=content)
        response = await HunterAPI.call(request)
        HunterAPI.log_message(response.text)

        return response
