import os
import pytest

import main


@pytest.mark.parametrize('decode_file, message, encode_file', [
    ('parrots.bmp', 'Hello World!', 'new_parrots.bmp'),
    ('cat.jpg', 'Test very long message to be sure my program will always work properly '
                'in the picture i can see a white cat and a green grass', 'new_cat.jpg'),
    ('poppies.bmp', 'Test many chars %(*&:"123+`', 'new_poppies.bmp'),
    ('ladybug.bmp', '', 'new_ladybug.bmp')
])
def test_encode_and_decode_message(decode_file, message, encode_file):
    main.hide_message(decode_file, message)
    assert main.read_message(encode_file) == message
    os.remove(encode_file)


@pytest.mark.parametrize('decode_file, message, encode_file', [
    ('parrots.jpg', 'Hello World!', 'new_parrot.bmp'),
    ('parrots', 'Hello World!', 'new_parrots'),
])
def test_wrong_picture(decode_file, message, encode_file):
    with pytest.raises(IOError):
        main.hide_message(decode_file, message)
        main.read_message(encode_file)


@pytest.mark.parametrize('message', [
    142, 50.00, pytest, {'a': 123}, ['a', 'b', 'c'], {'a', 'b', '123'}, pytest
])
def test_wrong_message(message):
    with pytest.raises(TypeError):
        assert main.hide_message('ladybug.bmp', message)
