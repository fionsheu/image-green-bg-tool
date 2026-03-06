
from rembg import remove
from PIL import Image
import numpy as np

TARGET_SIZE = (96, 74)


def process_image(input_path, output_path):

    img = Image.open(input_path)

    img = remove(img)
    img = img.convert("RGBA")

    data = np.array(img)

    r, g, b, a = data.T
    transparent = (a == 0)

    data[..., :-1][transparent.T] = (0,255,0)

    img = Image.fromarray(data)

    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    #img = img.resize(TARGET_SIZE)

    img.save(output_path)
