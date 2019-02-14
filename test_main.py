import pytest
import main


@pytest.mark.parametrize('decode_file, message, encode_file', [
    ('p.bmp', 'Hello World!', 'new_p.bmp')
])
def test_main(decode_file, message, encode_file):
    main.hide_message(decode_file, message)
    assert main.read_message(encode_file) == message
