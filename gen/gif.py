from glob import glob
import math
import os
from typing import Sequence
import subprocess

import numpy as np
from pygl import render, Model
import numgl
import png
import image
import npchr

def create_gif(files: Sequence[str], out: str):
    cmd = ['convert', '-delay', '5', '-dispose', 'previous']
    cmd.extend(files)
    cmd.append(out)
    subprocess.run(cmd, check=True)

def main():
    eye = np.array([0, 0, -1])
    target = np.array([0, 0, 0])
    up = np.array([0, 1, 0])

    cube = Model.load_obj('icosaedron.obj')
    cube.compute_face_normals()

    w = 64
    h = 64

    os.makedirs('images', exist_ok=True)
    n = 100
    tau = 2 * math.pi
    for a in range(n):
        eye = np.array([math.sin(tau * a / n), 0, math.cos(tau * a / n)])
        im = np.zeros((h, w, 4), 'uint8')
        render(im, cube, numgl.lookat(eye, target, up))
        with open('images/{:02}.png'.format(a), 'wb') as f:
            f.write(png.write(im.tobytes(), w, h))

    out = 'out.gif'
    create_gif(sorted(glob('images/*.png')), out)
    print(out)

main()
