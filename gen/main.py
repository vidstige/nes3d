from typing import List, Tuple

import numpy as np
from pygl import render, Model
import numgl
import png
import image
import npchr


Sprite = np.array
Lookup = List[Tuple[int, bool, bool]]

def make_lookup(n: int) -> Lookup:
    return [(i, False, False) for i in range(n)]


def optimize(sprites: List[Sprite], lookup: Lookup):
    return sprites, lookup


# Lookup format
# 64 bytes each
# * 32 bytes of tile indices (note - low bit is low/high page)
# * 32 Bytes of attreibutes, containg palette and vertical/horizontal flips
def pack_lookup(lookup: Lookup) -> bytes:
    indices = bytearray()
    attributes = bytearray()
    for index, horizontal, vertical in lookup:
        indices.append(index << 1)
        attributes.append(horizontal << 7 | vertical << 6)  # no flip
    return bytes(indices + attributes)


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
    tiles = list(image.tile(im2bit, shape=large))

    lookup = make_lookup(len(tiles))

    optimized_tiles, optimized_lookup = optimize(tiles, lookup)
    sprite_sheet = np.vstack(optimized_tiles)

    # write sprite sheet
    with open('image.chr', 'wb') as f:
        npchr.write(f, sprite_sheet)

    # write lookup tables
    with open('lookup.bin', 'wb') as f:
        f.write(pack_lookup(optimized_lookup))

main()
