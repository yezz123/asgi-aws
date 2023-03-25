from base64 import b64decode, b64encode
from typing import Any, Dict, Iterator
from urllib.parse import urlencode

from asgi_aws.services.http import Http
from asgi_aws.type import Message, Scope

Request = Dict[str, Dict[str, Any]]

Response = Dict[str, Any]


class AWS(Http[Request, Response]):
    """
    AWS Lambda HTTP API or REST API, or with Function URL ✨
    """

    @property
    def scope(self) -> Scope:
        event = self.request["event"]

        def generate_query() -> Iterator[str]:
            if "multiValueQueryStringParameters" in event:
                params = event["multiValueQueryStringParameters"] or {}
                for key, values in params.items():
                    for vale in values:
                        yield urlencode({key: vale})
            elif "queryStringParameters" in event:
                params = event["queryStringParameters"] or {}
                for key, values in params.items():
                    for vale in values.split(","):
                        yield urlencode({key: vale})
            return

        query_string = "&".join(generate_query()).encode()

        if "httpMethod" in event:
            method = event["httpMethod"]
        else:
            method = event["requestContext"]["http"]["method"]

        if "path" in event:
            path = event["path"]
        else:
            path = event["requestContext"]["http"]["path"]

        if "multiValueHeaders" in event:
            headers = tuple(
                (k.lower().encode("latin-1"), (",".join(vs)).encode("latin-1"))
                for k, vs in event["multiValueHeaders"].items()
            )
        else:
            headers = tuple(
                (k.lower().encode("latin-1"), v.encode("latin-1"))
                for k, v in event["headers"].items()
            )

        if "cookies" in event:
            cookies = ";".join(event["cookies"])
            headers = headers + ((b"cookie", cookies.encode("latin-1")))  # type: ignore

        return {
            "type": "http",
            "asgi": {"version": "3.0", "spec_version": "2.2"},
            "http_version": "1.1",
            "method": method,
            "scheme": "http",
            "path": path,
            "query_string": query_string,
            "headers": headers,
            "server": None,
            "client": None,
        }

    async def receive(self) -> Message:
        event = self.request["event"]
        body = event.get("body", "")

        if body is None:
            body = b""
        elif event.get("isBase64Encoded", False):
            body = b64decode(body)
        else:
            body = body.encode()
        return {
            "type": "http.request",
            "body": body,
            "more_body": False,
        }

    @property
    def response(self) -> Response:
        event = self.request["event"]
        if "version" in event:
            is_base64_encoded = True
            body = b64encode(self.body).decode()
        else:
            is_base64_encoded = False
            try:
                body = self.body.decode()
            except UnicodeDecodeError:
                is_base64_encoded = True
                body = b64encode(self.body).decode()
        return {
            "statusCode": self.status_code,
            "headers": dict(self.headers),
            "body": body,
            "isBase64Encoded": is_base64_encoded,
        }
