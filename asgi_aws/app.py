from typing_extensions import Protocol

from asgi_aws.type import Message, Receive, Request, Response, Scope, Send


class ASGIApp(Protocol):
    """ASGI Application, which is a callable that accepts a call function."""

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        ...


class ASGICycle(Protocol):
    """ASGI Cycle, which is a callable that accepts a send, a receive and a run function."""

    def __init__(self, request: Request) -> None:
        ...  # pragma: nocover

    def __call__(self, app: ASGIApp) -> None:
        ...  # pragma: nocover

    async def run(self, app: ASGIApp) -> None:
        ...  # pragma: nocover

    async def receive(self) -> Message:
        ...  # pragma: nocover

    async def send(self, message: Message) -> None:
        ...  # pragma: nocover

    @property
    def scope(self) -> Scope:
        ...  # pragma: nocover

    @property
    def response(self) -> Response:
        ...  # pragma: nocover
