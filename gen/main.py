import hashlib
from typing import List, Tuple
import os

import numpy as np
from pygl import render, Model
import numgl
import png
import image
import npchr


def md5(b: bytes) -> str:
    m = hashlib.md5()
    m.update(b)
    return m.digest().hex()[:7]


Sprite = np.array
class Lookup(object):
    def __init__(self, index, horizontal=False, vertical=False):
        self.index = index
        self.horizontal = horizontal
        self.vertical = vertical

    def __repr__(self) -> str:
        return 'Lookup({}, {}, {})'.format(self.index, self.horizontal, self.vertical)


def make_lookup(start: int, n: int) -> List[Lookup]:
    return [Lookup(i) for i in range(start, start + n)]


def diff(a: np.array, b: np.array) -> float:
    d = a - b
    return np.linalg.norm(d)


def replace_duplicates(sprites: List[Sprite], lookup: List[Lookup]):
    """Searches through tiles and replaces duplicates."""
    threshold = 0.8
    for i in lookup:
        sprite = sprites[i.index]
        for j, other in enumerate(sprites):
            # exact match
            if diff(sprite, other) < threshold:
                i.index = j
                i.horizontal = False
                i.vertical = False
                break
            # upside down
            if diff(np.flip(sprite, 1), other) < threshold:
                i.index = j
                i.horizontal = False
                i.vertical = True
                break
            # left-right
            if diff(np.flip(sprite, 0), other) < threshold:
                i.index = j
                i.horizontal = True
                i.vertical = False
                break
            if diff(np.flip(np.flip(sprite, 0), 1), other) < threshold:
                i.index = j
                i.horizontal = True
                i.vertical = True
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
    result = bytearray()
    for l in lookup:
        result.append(l.index & 0xff)
        result.append(l.horizontal << 7 | l.vertical << 6)
    return bytes(result)


def main():
    target = np.array([0, 0, 0])
    up = np.array([0, 1, 0])

    cube = Model.load_obj('icosaedron.obj')
    cube.compute_face_normals()

    w = 64
    h = 64

    n = 32
    tiles = []
    for i in range(n):
        a = 2*np.pi * i / n
        eye = np.array([np.sin(a), 0, np.cos(a)])
        projection = numgl.lookat(eye, target, up)
        projection_hash = md5(projection.data.tobytes())
        cache_file = 'cache/render-{hash}.npy'.format(hash=projection_hash)
        if os.path.isfile(cache_file):
            im = np.load(cache_file)
        else:
            im = np.zeros((h, w, 4))
            render(im, cube, projection)
            os.makedirs('cache/', exist_ok=True)
            np.save(cache_file, im)

        #with open('image-{:02}.png'.format(i), 'wb') as f:
        #    f.write(png.write(image.quantize(im, bits=8).tobytes(), w, h))

        large = (8, 16)
        tiles.extend(image.tile(im, shape=large))
    
    lookup = make_lookup(0, len(tiles))

    replace_duplicates(tiles, lookup)
    repack(tiles, lookup)

    # downsample to 2-bits
    # write sprite sheets
    low_bank = image.quant2(image.intensity(np.vstack(tiles[0::2])), bits=2)
    with open('image-0000.chr', 'wb') as f:
        f.write(npchr.write(low_bank))

    high_bank = image.quant2(image.intensity(np.vstack(tiles[1::2])), bits=2)
    with open('image-1000.chr', 'wb') as f:
        f.write(npchr.write(high_bank))

    # write lookup tables
    with open('lookup.bin', 'wb') as f:
        f.write(pack_lookup(lookup))

main()
