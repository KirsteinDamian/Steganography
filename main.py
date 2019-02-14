from PIL import Image
import binascii


def str2bin(mes):
    return bin(int(binascii.hexlify(mes), 16))[2:]


def bin2str(binary):
    return binascii.unhexlify('0b{:02x}'.format(int(binary, 2)))[1:]


def hide_message(filename, message):
    try:
        with Image.open(filename) as image:
            bin_message = str2bin(message) + '11111111111111111110'
            bin_position = 0
            new_pixels = []
            if image.mode in 'RGB':
                new_img = image.convert('RGB')
                pixels = new_img.getdata()

                for pix in pixels:
                    if bin_position < len(bin_message):
                        blue_part = bin(pix[2])
                        blue_part = blue_part[:-1] + bin_message[bin_position]
                        new_pix = (pix[0], pix[1], int(blue_part, 2))
                        new_pixels.append(new_pix)
                        bin_position += 1
                    else:
                        break

                new_img.putdata(new_pixels)
                new_img.save('new_'+filename, 'PNG')
                return 'Completed!'
            return 'Wrong mode of picture!'

    except IOError:
        raise IOError("{} couldn't be opened, check if name is correct.".format(filename))


def read_message(filename):
    try:
        with Image.open(filename) as image:
            bin_message = ''
            pixels = image.getdata()
            if image.mode in 'RGB':

                for pix in pixels:
                    bin_message += bin(pix[2])[-1]
                    if bin_message[-20:] == '11111111111111111110':
                        return bin2str(bin_message[:-20])
            return 'Wrong mode of picture!'
    except IOError:
        print "{} couldn't be opened, check if name is correct.".format(filename)
