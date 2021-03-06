import argparse
import binascii

from PIL import Image


INVALID_FILENAME = '{} could not be opened, check if name is correct.'
INVALID_MESSAGE_TYPE = 'Message has to be a string!'
INVALID_IMAGE_MODE = 'Wrong mode of the image!'


def string_to_binary(message):
    """
    Convert string text to binary string
    :param message: string message we want to convert
    :return: string binary message without '0b' on beginning
    """
    return bin(int(binascii.hexlify(message), 16))[2:] if message != '' else ''


def binary_to_string(binary):
    """
    Convert string with binary message to text message
    :param binary: string with binary message WITHOUT '0b' on beginning
    :return: string message
    """
    return binascii.unhexlify('0b{:02x}'.format(int(binary, 2)))[1:] if binary != '' else ''


def encode_message(filename, message):
    """
    Hide text message in the picture. String text is converted into binary code and
    successive bits replace LSB in the blue part of the pixels.
    :param filename: name of image in which the method hide the message
    :param message: string text message which will be hide in picture
    :return: string message 'Completed!' or raise error
    """
    if type(message) != str:
        raise TypeError(INVALID_MESSAGE_TYPE)
    try:
        with Image.open(filename) as image:
            bin_message = string_to_binary(message) + '11111111111111111110'
            bin_position = 0
            new_pixels = []
            if image.mode in 'RGB':
                image = image.convert('RGB')
                pixels = image.getdata()

                for pixels in pixels:
                    if bin_position < len(bin_message):
                        blue_part = bin(pixels[2])
                        blue_part = blue_part[:-1] + bin_message[bin_position]  # swap pixel
                        new_pix = (pixels[0], pixels[1], int(blue_part, 2))
                        new_pixels.append(new_pix)
                        bin_position += 1
                    else:
                        break

                image.putdata(new_pixels)
                image.save('new_' + filename, 'PNG')
                return 'Completed!'
            else:
                raise TypeError(INVALID_IMAGE_MODE)
    except IOError:
        raise IOError(INVALID_FILENAME.format(filename))


def decode_message(filename):
    """
    Decode the message in the image.
    :param filename: name of the image with hidden message
    :return: if decoding succeeds return string hidden message, else raise error
    """
    try:
        with Image.open(filename) as image:
            bin_message = ''
            pixels = image.getdata()
            if image.mode in 'RGB':

                for pixels in pixels:
                    bin_message += bin(pixels[2])[-1]
                    if bin_message[-20:] == '11111111111111111110':
                        return binary_to_string(bin_message[:-20])
            else:
                raise TypeError(INVALID_IMAGE_MODE)
    except IOError:
        raise IOError(INVALID_FILENAME.format(filename))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', help='Name of image in which the method hide the message',
                        type=str, required=True)
    parser.add_argument('-m', '--message', help='String text message which will be hide in picture',
                        type=str)
    args = parser.parse_args()
    if args.message:
        encode_message(args.filename, args.message)
    else:
        print decode_message(args.filename)
