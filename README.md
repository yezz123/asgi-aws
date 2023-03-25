# asgi-aws

![logo](https://raw.githubusercontent.com/yezz123/asgi-aws/main/.github/logo.png)

<p align="center">
<a href="https://github.com/yezz123/asgi-aws/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/yezz123/asgi-aws/actions/workflows/test.yml/badge.svg" alt="Test">
</a>
<a href="https://github.com/yezz123/asgi-aws/actions/workflows/lint.yml">
    <img src="https://github.com/yezz123/asgi-aws/actions/workflows/lint.yml/badge.svg"/>
</a>
<a href="https://codecov.io/gh/yezz123/asgi-aws">
    <img src="https://codecov.io/gh/yezz123/asgi-aws/branch/main/graph/badge.svg?token=MTG51U77R2"/>
</a>
<a href="https://github.com/yezz123/asgi-aws/actions/workflows/lint.yml">
    <img src="https://github.com/yezz123/asgi-aws/actions/workflows/lint.yml/badge.svg"/>
</a>
<a href="https://pypi.org/project/asgi_aws">
    <img src="https://img.shields.io/pypi/pyversions/asgi_aws.svg?color=%2334D058"/>
</a>
</p>

Build API with ASGI in AWS Lambda with API Gateway HTTP API or REST API, or with Function URL ✨

## Installation

```sh
pip install asgi_aws
```

## Example

- Create a file `main.py` with:

```python
from asgi_aws import Asgi
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

entry_point = Asgi.entry_point(app)
```

## Deploy it

- Let's create for example a yaml file with the following content:

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31

Resources:
  ExFunctionUrlAPI:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.10
      CodeUri: src/
      Handler: main.entry_point
      MemorySize: 256
      Timeout: 30
      FunctionUrlConfig:
        AuthType: NONE
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
# Install dependencies
pip install -e .[test,lint]
```

### Run tests 🌝

You can run all the tests with:

```bash
bash scripts/test.sh
```

### Format the code 🍂

Execute the following command to apply `pre-commit` formatting:

```bash
bash scripts/format.sh
```

Execute the following command to apply `mypy` type checking:

```bash
bash scripts/lint.sh
```

## License

This project is licensed under the terms of the MIT license.
