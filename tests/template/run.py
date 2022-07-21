from asgi_aws import Asgi, AsgiService
from tests.template.app import app

entry_point = Asgi.entry_point(app, AsgiService.aws)
