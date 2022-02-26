import cv2# used for images
import numpy as np


def rgb_to_hex(r, g, b):
    """takes rgb parameters and converts them to a hex code"""
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def hex_to_rgb(hex_val):
    """takes a hex code and it as a string of an rgb value in the format (r, g, b)"""
    hex_val = hex_val.lstrip('#'); lv = len(hex_val)
    hex_val = str(tuple((int(hex_val[i:i + lv // 3], 16)) for i in range(0, lv, lv // 3)))
    return hex_val# this is returning the rgb, the variable name is just never changed


def invert_colour(value):
    """takes a hex value and inverts the colour of it, which is returned as a hex code"""
    value = value.lstrip("#")
    return rgb_to_hex(abs(int(value[0:2], 16) - 255), abs(int(value[2:4], 16) - 255), abs(int(value[4:6], 16) - 255))


def alter_colour(value, shade_factor):
    """takes a hex value and changes it by a shading factor, used to alter colours in the program"""
    value = value.lstrip('#'); len_value = len(value)
    value = str(tuple((int(value[i:i + len_value // 3], 16))+1 for i in range(0, len_value, len_value // 3)))
    try:# try was used here since MOST cases work like this
        ret_val = rgb_to_hex((int(int(value[1:4]) * (1-shade_factor))), (int(int(value[6:9]) * (1-shade_factor))), (int(int(value[11:14]) * (1-shade_factor))))
        if len(ret_val) == 7:
            return ret_val
        else:
            return ret_val[:7]

    except ValueError:# caused by any of the r/g/b values being under 100
        values = value.lstrip("(").rstrip(")").replace(" ", "").split(",")
        for i in range(len(values)):
            if len(values[i]) == 2:# this fixes the length of the number part so no error is caused when grabbing the numbers from a string
                values[i] = "0" + values[i]
            elif len(values[i]) == 1:
                values[i] = "00" + values[i]
        ret_val = rgb_to_hex(int((int(values[0]) * (1-shade_factor))), int((int(values[1]) * (1-shade_factor))), int((int(values[2]) * (1-shade_factor))))
        if len(ret_val) == 7:
            return ret_val
        else:
            return ret_val[:7]


def change_border_colour(hex, name):
    """takes a hex value for a border and creates an image of a border in this colour"""
    rgb = hex_to_rgb(hex).lstrip("(").rstrip(")").replace(" ", "").split(",")
    m = cv2.imread(r"Images\border_template.png")
    h, w, bpp = np.shape(m)
    for py in range(0, h):
        for px in range(0, w):
            if m[py][px][0] > 0:
                m[py][px][2] = int(rgb[0])
                m[py][px][1] = int(rgb[1])
                m[py][px][0] = int(rgb[2])
    cv2.imwrite(fr"Images\border_{name}.png", m)
    bgra = cv2.cvtColor(cv2.imread(fr"Images\border_{name}.png"), cv2.COLOR_BGR2BGRA)
    alpha = bgra[:, :, 3]
    alpha[np.all(bgra[:, :, 0:3] == (0, 0, 0), 2)] = 0
    cv2.imwrite(fr"Images\border_{name}.png", bgra)


# ↓ debug ↓
if __name__ == '__main__':
    print(alter_colour("#FFFFFFFF00", -10))