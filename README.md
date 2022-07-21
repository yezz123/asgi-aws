# asgi-aws

[![Tests](https://github.com/yezz123/asgi-aws/actions/workflows/test.yml/badge.svg)](https://github.com/yezz123/asgi-aws/actions/workflows/test.yml)
[![Lint and Format](https://github.com/yezz123/asgi-aws/actions/workflows/lint.yml/badge.svg)](https://github.com/yezz123/asgi-aws/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/yezz123/asgi-aws/branch/main/graph/badge.svg?token=MTG51U77R2)](https://codecov.io/gh/yezz123/asgi-aws)
[![Language](https://img.shields.io/badge/Language-Python-green?style)](https://github.com/yezz123)
[![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flatcolor=BC4E99)](https://github.com/yezz123/asgi-aws)
[![Pypi](https://img.shields.io/pypi/pyversions/asgi_aws.svg?color=%2334D058)](https://pypi.org/project/asgi_aws)

Build API with ASGI in AWS Lambda with API Gateway HTTP API or REST API, or with
Function URL ✨

## Installation

```sh
pip install asgi_aws
```

## Example

- Create a file `main.py` with:

```python
from asgi_aws import Asgi, AsgiService
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

entry_point = Asgi.entry_point(app, AsgiService.aws)
```

## Deploy it

- Let's create for exampple a yaml file with the following content:

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31

Resources:
  ExFunctionUrlAPI:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.9
      CodeUri: src/
      Handler: main.entry_point
      MemorySize: 256
      Timeout: 30
      FunctionUrlConfig:
        AuthType: NONE
      Environment:
        Variables:
          AsgiService: AWS Lambda
```

- Now, we can deploy the function with the following command:

```sh
# deploy HTTP API
sam build -t api.yaml --use-container
sam run deploy
```

**Note:** You can also deploy the function under Deployment for Rest API or with
a Function URL.

## Development 🚧

### Setup environment 📦

You should create a virtual environment and activate it:

```bash
python -m venv venv/
```

```bash
source venv/bin/activate
```

And then install the development dependencies:

```bash
# Install Flit
pip install flit

# Install dependencies
flit install --symlink
```

### Run tests 🌝

You can run all the tests with:

```bash
make test
```

### Format the code 🍂

Execute the following command to apply `pre-commit` formatting:

```bash
make lint
```

## License

This project is licensed under the terms of the MIT license.
