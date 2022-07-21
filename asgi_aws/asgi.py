import asyncio
from enum import Enum
from typing import Any, Callable, Type, Union

from asgi_aws.app import ASGIApp, ASGICycle
from asgi_aws.services.aws import AWS


class Service(str, Enum):
    """ASGI Service Type"""

    aws = "AWS Lambda"


class Asgi:
    """
    This is the main entry point for the ASGI server, which is called by the AWS Lambda runtime, or by the AWS API Gateway, or by the AWS API Gateway REST API, or by the AWS API Gateway HTTP API

    :param request: The request object, which is a dictionary containing the following keys:
        - `method`: The HTTP method, e.g. `GET`, `POST`, `PUT`, `DELETE`
        - `path`: The path of the request, e.g. `/`, `/hello`, `/hello/world`
        - `query_string`: The query string of the request, e.g. `foo=bar&baz=qux`
        - `headers`: The headers of the request, e.g. `{"Content-Type": "application/json"}`
        - `body`: The body of the request, e.g. `{"foo": "bar"}`
    :return: The response object, which is a dictionary containing the following keys:
        - `status`: The status code of the response, e.g. 200, 404, 500
        - `headers`: The headers of the response, e.g. `{"Content-Type": "application/json"}`
        - `body`: The body of the response, e.g. `{"foo": "bar"}`
    """

    def __init__(self, app: ASGIApp, http_cycle: Type[ASGICycle]):
        self.app = app
        self._http_cycle = http_cycle
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    def __call__(self, request: Any) -> Any:
        cycle = self._http_cycle(request)
        cycle(app=self.app)
        return cycle.response

    @classmethod
    def entry_point(
        cls, app: ASGIApp, service: Union[str, Service]
    ) -> Callable[..., Any]:
        """
        :param app: The ASGI Application
        :param service: The service type, which is either a string or an enum of type `Service`
        :return: The entry point for the ASGI server
        """
        if service == Service.aws:

            def entrypoint(event: Any, context: Any) -> Any:
                return cls(app, AWS)(request={"event": event, "context": context})

            return entrypoint

        else:
            service = ", ".join(map(lambda x: x.value, Service))  # pragma: nocover
            raise ValueError(f"Unknown service: {service}")  # pragma: nocover
