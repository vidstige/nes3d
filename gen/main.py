import numpy as np
from pygl import render, Model
import numgl
import png
import image
import npchr

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
    sprite_sheet = np.vstack(image.tile(im2bit, shape=large))

    # re-arrange
    with open('image.chr', 'wb') as f:
        npchr.write(f, sprite_sheet)

main()
