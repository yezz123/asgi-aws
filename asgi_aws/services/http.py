import asyncio
from typing import Generic, Iterable, Tuple, TypeVar

from asgi_aws.app import ASGIApp
from asgi_aws.type import Message, Scope

Req = TypeVar("Req")
Res = TypeVar("Res")


class Http(Generic[Req, Res]):
    """
    Class HTTP is a generic class for ASGI HTTP API or REST API, or with Function URL,
    Using This class give us the ability to use some functions like `send`, `run` and `receive`
    """

    def __init__(self, request: Req):
        self.request = request
        self.status_code = 200
        self.headers: Iterable[Tuple[str, str]] = ()
        self.body = b""

    def __call__(self, app: ASGIApp) -> None:
        loop = asyncio.get_event_loop()
        instance = self.run(app)
        task = loop.create_task(instance)
        loop.run_until_complete(task)

    @property
    def response(self) -> Res:
        raise NotImplementedError

    async def send(self, message: Message) -> None:
        if message["type"] == "http.response.start":
            self.status_code = message["status"]
            self.headers = tuple(
                (key.decode("latin-1"), value.decode("latin-1"))
                for (key, value) in message["headers"]
            )
        elif message["type"] == "http.response.body":
            self.body = message["body"]
        return None

    async def run(self, app: ASGIApp) -> None:
        await app(self.scope, self.receive, self.send)

    async def receive(self) -> Message:
        raise NotImplementedError

    @property
    def scope(self) -> Scope:
        raise NotImplementedError
