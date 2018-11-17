import numpy as np
from pygl import render, Model
import numgl
import png
import image
import npchr


def layout(sprite_sheets):
    lookup = list(range(32))
    return sprite_sheets[0], lookup


# Lookup format
# 64 bytes each
# * 32 bytes of tile indices (note - low bit is low/high page)
# * 32 Bytes of attreibutes, containg palette and vertical/horizontal flips
def pack_lookup(lookup) -> bytes:
    packed = bytearray()
    for tile_index in lookup:
        packed.append(tile_index << 1)
    for _ in range(32):
        packed.append(0)  # no flip
    return bytes(packed)


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
        f.write(pack_lookup(lookup))

main()
