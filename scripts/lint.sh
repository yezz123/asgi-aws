#!/usr/bin/env bash

set -e
set -x

mypy --show-error-codes asgi_aws
