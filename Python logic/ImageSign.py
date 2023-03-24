import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import jpeglib as jpglib
from exif import Image as eImage
import string

def hash():
    name = "Images/original.jpg"
    image = Image.open(name)
    if name[-4:] == '.png':
        image = image.convert('RGB')
    image = image.resize((300, 200))
    print(image.size)
    image.show()

hash()




