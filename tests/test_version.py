import asgi_aws


def test_version() -> None:
    assert asgi_aws.__version__ == "2.0.0"
