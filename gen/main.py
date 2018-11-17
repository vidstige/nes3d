import numpy as np
from pygl import render, Model
import numgl
import png
import image
import npchr

# lookup 16 bytes
# 11 bits needed for tile index (32k memory, each tile is 16 bytes)
# 2 bits needed flr flip status
def layout(sprite_sheets):
    lookup = bytes()
    return sprite_sheets[0], lookup


def main():
    eye = np.array([0, 0, -1])
    target = np.array([0, 0, 0])
    up = np.array([0, 1, 0])
    projection = numgl.lookat(eye, target, up)

    cube = Model.load_obj('icosaedron.obj')
    cube.compute_face_normals()

    w = 64
    h = 64
    im = np.zeros((h, w, 4), 'uint8')
    render(im, cube, projection)

    with open('image.png', 'wb') as f:
        f.write(png.write(im.tobytes(), w, h))

    # downsample to 2-bits
    im2bit = image.downsample(image.intensity(im), bits=2)

    large = (8, 16)
    sprite_sheet0 = np.vstack(image.tile(im2bit, shape=large))

    sprite_sheets = [sprite_sheet0]
    sprite_sheet, lookup = layout(sprite_sheets)

    # re-arrange
    with open('image.chr', 'wb') as f:
        npchr.write(f, sprite_sheet)

    # write lookups
    with open('lookup.bin', 'wb') as f:
        f.write(lookup)

main()
