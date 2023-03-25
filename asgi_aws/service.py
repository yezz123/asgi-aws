import os
from typing import Union

from asgi_aws.services import Service


def find_service() -> Union[Service, None]:
    # ref: https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html
    return Service.aws_lambda if "AWS_LAMBDA_FUNCTION_NAME" in os.environ else None
