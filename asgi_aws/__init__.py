"""Build API with ASGI in AWS Lambda with API Gateway HTTP API or REST API, or with Function URL ✨"""

__version__ = "1.0.0"

from asgi_aws.asgi import Asgi as Asgi
from asgi_aws.asgi import Service as AsgiService

__all__ = ["Asgi", "AsgiService"]
