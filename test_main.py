import os
import pytest

import main


@pytest.mark.parametrize('encode_file, message, decode_file', [
    ('parrots.bmp', 'Hello World!', 'new_parrots.bmp'),
    ('cat.jpg', 'Test very long message to be sure my program will always work properly '
                'in the picture i can see a white cat and green grass', 'new_cat.jpg'),
    ('poppies.bmp', 'Test many chars %(*&:"123+`', 'new_poppies.bmp'),
    ('ladybug.bmp', '', 'new_ladybug.bmp')
])
def test_encode_and_decode_message(encode_file, message, decode_file):
    main.encode_message(encode_file, message)
    assert main.decode_message(decode_file) == message
    os.remove(decode_file)


@pytest.mark.parametrize('encode_file, message', [
    ('parrots.jpg', 'Hello World!'),
    ('parrots', 'Hello World!'),
])
def test_encode_given_invalid_filename(encode_file, message):
    with pytest.raises(IOError) as error:
        main.encode_message(encode_file, message)
    assert main.INVALID_FILENAME.format(encode_file) == str(error.value)


@pytest.mark.parametrize('decode_file', [
    'new_parrot.bmp',
    'new_parrots',
])
def test_decode_given_invalid_filename(decode_file):
    with pytest.raises(IOError) as error:
        main.decode_message(decode_file)
    assert main.INVALID_FILENAME.format(decode_file) == str(error.value)


@pytest.mark.parametrize('message', [
    142, 50.00, pytest, {'a': 123}, ['a', 'b', 'c'], {'a', 'b', '123'}, pytest
])
def test_invalid_type_of_message(message):
    with pytest.raises(TypeError) as error:
        main.encode_message('ladybug.bmp', message)
    assert main.INVALID_MESSAGE_TYPE == str(error.value)


def test_invalid_image_mode():
    with pytest.raises(TypeError) as error:
        main.encode_message('cmyk_mode.bmp', 'Hello World!')
    assert main.INVALID_IMAGE_MODE == str(error.value)
