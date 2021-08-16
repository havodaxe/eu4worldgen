"""
Module that holds the generate_seeds function
"""

from random import seed, randint
from PIL import Image
import numpy as np

def generate_seeds(land=True):
    """
    Generate an image consisting of random dispersed dots, to be used as
    input for the province generator.
    """
    INITRED = 0
    INITGREEN = 0
    INITBLUE = 0
    seed(0)
    seed_coords = []

    out = Image.new("RGBA", (5632,2048), (0,0,0,255))
    if(land == True):
        redmodulus = 192
        redminimum = 48
        greenmodulus = 192
        greenminimum = 48
        bluemodulus = 32
        blueminimum = 0
    else:
        redmodulus = 32
        redminimum = 0
        greenmodulus = 64
        greenminimum = 64
        bluemodulus = 128
        blueminimum = 128

    for i in range(1600):
        seed_coords.append(( randint(0, out.width - 1),
                             randint(0, out.height - 1) ))
        red =   (INITRED   + 13 * i + i // 256)   % redmodulus + redminimum
        green = (INITGREEN + 17 * i + i // 65536) % greenmodulus + greenminimum
        blue =  (INITBLUE  + 19 * i)              % bluemodulus + blueminimum
        # After each loop through the 256 colour values, red shifts over by 1
        # And after 256 * 256 loops, green shifts over by 1
        # This process ensures that eventually, each colour gets visited.
        # The prime numbers are just to make it look nicer and similar to how
        # it was before.
        out.putpixel(seed_coords[i], (red, green, blue, 0))
        # Alpha is distance to seed

    print(len(seed_coords))

    if __name__ == '__main__':
        out.save("seed_img.png")

    seed_image_bytes = out.tobytes()
    ndarray_bytes = np.frombuffer(seed_image_bytes, np.uint8)
    ndarray_floats_255 = np.array(ndarray_bytes, np.float_)
    return ndarray_floats_255 / 255

if __name__ == '__main__':
    generate_seeds()
