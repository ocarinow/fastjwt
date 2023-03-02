import base64


def decode_base64_key(key: str) -> str:
    return base64.standard_b64decode(key).decode()
