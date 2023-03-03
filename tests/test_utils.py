import pytest

from fastjwt.utils.secrets import decode_base64_key


def test_decode_base64_key():
    ENCODED_STRING = "QmFzZTY0IEVuY29kZWQgU3RyaW5n"
    DECODED_STRING = decode_base64_key(ENCODED_STRING)
    assert isinstance(DECODED_STRING, str), "Decoded b64 is not a string"
    assert DECODED_STRING == "Base64 Encoded String", "Mismatch on decoding b64 string"
