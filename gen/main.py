from typing import List, Tuple

import numpy as np
from pygl import render, Model
import numgl
import png
import image
import npchr


Sprite = np.array
class Lookup(object):
    def __init__(self, index, horizontal=False, vertical=False):
        self.index = index
        self.horizontal = horizontal
        self.vertical = vertical

    def __repr__(self) -> str:
        return 'Lookup({}, {}, {})'.format(self.index, self.horizontal, self.vertical)


def make_lookup(n: int) -> List[Lookup]:
    return [Lookup(i) for i in range(n)]


def replace_duplicates(sprites: List[Sprite], lookup: List[Lookup]):
    """Searches through tiles and replaces duplicates."""
    for i in lookup:
        for j, sprite in enumerate(sprites):
            if (sprites[i.index] == sprite).all():
                i.index = j
                break


def repack(sprites: List[Sprite], lookup: List[Lookup]):
    """Remove unused sprites"""
    remap = {}
    all_sprites = sprites.copy()
    sprites.clear()
    for l in lookup:
        new_index = remap.get(l.index)
        if not new_index:
            sprites.append(all_sprites[l.index])
            new_index = len(sprites) - 1
            remap[l.index] = new_index
        l.index = new_index


# Lookup format
# 64 bytes each
# * 32 bytes of tile indices (note - low bit is low/high page)
# * 32 Bytes of attreibutes, containg palette and vertical/horizontal flips
def pack_lookup(lookup: List[Lookup]) -> bytes:
    indices = bytearray()
    attributes = bytearray()
    for l in lookup:
        indices.append(l.index << 1)
        attributes.append(l.horizontal << 7 | l.vertical << 6)  # no flip
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

    replace_duplicates(tiles, lookup)
    repack(tiles, lookup)

    sprite_sheet = np.vstack(tiles)

    # write sprite sheet
    with open('image.chr', 'wb') as f:
        npchr.write(f, sprite_sheet)

    # write lookup tables
    with open('lookup.bin', 'wb') as f:
        f.write(pack_lookup(lookup))

main()
