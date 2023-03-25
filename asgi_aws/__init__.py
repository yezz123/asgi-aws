"""Build API with ASGI in AWS Lambda with API Gateway HTTP API or REST API, or with Function URL ✨"""

__version__ = "2.0.0"

import asyncio
from typing import Any, Callable, Type, Union

from asgi_aws.service import find_service
from asgi_aws.services import Service
from asgi_aws.services.aws import AWS
from asgi_aws.types import ASGIApp, ASGICycle


class Asgi:
    """
    This is the main entry point for the ASGI server, which is called by the AWS Lambda runtime, or by the AWS API Gateway, or by the AWS API Gateway REST API, or by the AWS API Gateway HTTP API
    """

    def __init__(self, app: ASGIApp, http_cycle: Type[ASGICycle]) -> None:
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
        cls, app: ASGIApp, service: Union[str, Service, None] = None
    ) -> Callable[..., Any]:
        """
        :param app: The ASGI Application
        :param service: The service type, which is either a string or an enum of type `Service`
        :return: The entry point for the ASGI server
        """
        if service is None:
            service = find_service()

            def entrypoint(event: Any, context: Any) -> Any:
                return cls(app, AWS)(request={"event": event, "context": context})

            return entrypoint

        else:
            service = ", ".join(x.value for x in Service)
            raise ValueError(f"Unknown service: {service}")
