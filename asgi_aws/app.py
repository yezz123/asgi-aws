from typing_extensions import Protocol

from asgi_aws.type import Message, Receive, Request, Response, Scope, Send


class ASGIApp(Protocol):
    """ASGI Application, which is a callable that accepts a call function."""

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        ...


class ASGICycle(Protocol):
    """ASGI Cycle, which is a callable that accepts a send, a receive and a run function."""

    def __init__(self, request: Request) -> None:
        ...

    def __call__(self, app: ASGIApp) -> None:
        ...

    async def run(self, app: ASGIApp) -> None:
        ...

    async def receive(self) -> Message:
        ...

    async def send(self, message: Message) -> None:
        ...

    @property
    def scope(self) -> Scope:
        ...

    @property
    def response(self) -> Response:
        ...
