import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import jpeglib as jpglib
from exif import Image as eImage
import string
from copy import deepcopy
import hashlib

OFFSET = 2**9
MASK = 0b1111_1101_1111_1111 #(2**16 - 1) &~ OFFSET
ANTIMASK = 0b0000_0010_0000_0000
print("{0:b}".format(ANTIMASK))
def hash(im, blocks = 16):
    """def hash_block(Cb, Cr, Y):
        value = np.concatenate((Cb.flatten(), Cr.flatten(), Y.flatten())).flatten()
        value = np.bitwise_and(value, 0b1111_1111_1111_1110)
        return hashlib.sha256(''.join([str(v) for v in value]).encode('utf-8')).hexdigest()


    x, y = np.shape(im.Cb)[0:2] // np.array([4, 4])   #int(np.sqrt(blocks))
    xY, yY = np.shape(im.Y)[0:2] // np.array([4, 4])
    blocks = []

    for n in range(4):
        for m in range(4):
            blocks.append(hash_block(im.Cb[x * m: x * (m + 1) if m<3 else None, y * n: y * (n + 1) if n<3 else None,:,:],
                                      im.Cr[x * m: x * (m + 1) if m<3 else None, y * n: y * (n + 1) if n<3 else None,:,:],
                                      im.Y[xY * m: xY * (m + 1) if m<3 else None, yY * n: yY * (n + 1) if n<3 else None,:,:]
                                     ))
    #merge hashes
    block = hashlib.sha256(''.join(blocks).encode('utf-8')).hexdigest()"""

    value = np.concatenate((im.Cb.flatten(), im.Cr.flatten(), im.Y.flatten()))
    value = np.bitwise_and(value, MASK)
    return hashlib.sha256(''.join([str(v) for v in value]).encode("ascii")).hexdigest()


def sign(im, block):
    for k in range(4):
        for x in range(8):
            val = int(block[(k * 8 + x) * 2: (k * 8 + x) * 2 + 2], base=16)
            for y in range(8):
                im.Cb[0, k, x, y] &= MASK
                im.Cb[0, k, x, y] |= bool(2**y & val) * OFFSET

def get_signature(im):
    def numberToStr(n):
        ar = [str(a) for a in range(10)] + ['a', 'b', 'c', 'd', 'e', 'f']
        digits = ''
        for _ in range(2):
            digits = ar[n % 16] + digits
            n //= 16
        return digits
    signature = ""
    for k in range(4):
        for x in range(8):
            val = 0
            for y in range(8):
                v = bool(im.Cb[0, k, x, y] & ANTIMASK)
                val += 2**y * v
            signature += numberToStr(val)
    return signature




original = jpglib.read_dct("Images/original_hq.jpg")

print("Hash:" + hash(original))
sign(original, hash(original))

print("Signatur im Original:" + get_signature(original))

original.write_dct("Images/signiert_hq.jpg")
bearbeitet = jpglib.read_dct("Images/signiert_hq.jpg")

print("Signatur im bearbeiteten:" + get_signature(bearbeitet))
print("Hash im bearbeiteten:" + hash(bearbeitet))
w = jpglib.read_dct("Images/w.jpg")
print("signatur whatsapp:" + get_signature(w))
print("hash whatsapp:" + hash(w))








#original.write_dct('other.jpg')
#for k in hash(original): print(k in hash(bearbeitet))
#original = np.array(Image.open("Images/original.jpg"))
#other = np.array(Image.open("Images/twitter_dct.jpg"))
#print(np.sum(original - other))
