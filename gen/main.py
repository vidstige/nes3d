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

    im = np.zeros((64, 64, 4), 'uint8')
    render(im, cube, projection)

    with open('image.png', 'wb') as f:
        f.write(png.write(im.tobytes(), 64, 64))

    # downsample to 2-bits
    im2bit = image.downsample(image.intensity(im), bits=2)

    # re-arrange
    with open('image.chr', 'w') as f:
        npchr.write(f, im2bit)

main()
