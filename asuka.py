#!/usr/bin/env python3
from PIL import Image
import numpy as np
import os, sys


ascii_chars = "@@@%%%###***+++===---:::...!!!/// "

def map_luminosity_to_ascii(luminosity_matrix, ascii_chars):
    # Normalize luminosity values to the range of the ASCII characters
    normalized_luminosity = (luminosity_matrix - luminosity_matrix.min()) / (luminosity_matrix.max() - luminosity_matrix.min())
    indices = (normalized_luminosity * (len(ascii_chars) - 1)).astype(int)
    ascii_matrix = np.array([[ascii_chars[idx] for idx in row] for row in indices])
    return ascii_matrix

def print_ascii_art(ascii_matrix):
    for row in ascii_matrix:
        print(str("".join(row)))


# base_width = 128
# img = Image.open('/home/adrian/Downloads/asuka_original.jpg')
# wpercent = (base_width / float(img.size[0]))
# hsize = int((float(img.size[1]) * float(wpercent)))
# img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
# img.save('/home/adrian/Downloads/asuka_original_resized.jpg')


size = 100, 100

im = Image.open("/home/adrian/Downloads/asuka_original.jpg")
im.thumbnail(size, Image.Resampling.LANCZOS)
im.save("asuka_original_resized.jpg")       


print(im.format, im.size, im.mode)
pixel_matrix = np.array(im)
print(pixel_matrix)

luminosity_matrix = 0.21 * pixel_matrix[:, :, 0] + 0.72 * pixel_matrix[:, :, 1] + 0.07 * pixel_matrix[:, :, 2]

print(luminosity_matrix)

ascii_matrix = map_luminosity_to_ascii(luminosity_matrix, ascii_chars)

string_ascii = print_ascii_art(ascii_matrix) 

print_ascii_art(ascii_matrix)

for y, line in enumerate(ascii_matrix, 2):
    print(ascii_matrix)

  
