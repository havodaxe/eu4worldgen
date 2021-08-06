"""
Generate an image consisting of random dispersed dots, to be used as
input for the province generator.

Of interest are seed_image_bytes and seed_image_norm_floats.
"""

from random import seed, randint
from PIL import Image
import numpy as np

red = 0
green = 85
blue = 170
# By keeping the colours offset like this we ensure that the first few
# colours at least are saturated and not complete black
seed(0)
seed_coords = []

out = Image.new("RGBA", (5632,2048), (0,0,0,255))

for i in range(1600):
    seed_coords.append(( randint(0, out.width - 1),
                         randint(0, out.height - 1) ))
    out.putpixel(seed_coords[i], (red, green, blue, 0)) # Alpha is distance
    red = (red + 13) % 256
    green = (green + 17) % 256
    blue = (blue + 19) % 256
    # Like periodical cicadas. Not sure how rigorous this approach is.

print(len(seed_coords))

if __name__ == '__main__':
    out.save("seed_img.png")

seed_image_bytes = out.tobytes()
ndarray_bytes = np.frombuffer(seed_image_bytes, np.uint8)
ndarray_floats_255 = np.array(ndarray_bytes, np.float_)
seed_image_norm_floats = ndarray_floats_255 / 255
