from typing import Sequence, Tuple
import numpy as np


def intensity(img: np.array) -> np.array:
    return np.mean(img, axis=-1)


def _type_for_bit_width(bits: int) -> str:
    if bits > 32:
        return 'uint64'
    if bits > 16:
        return 'uint32'
    if bits > 8:
        return 'uint16'
    return 'uint8'


def quantize(img: np.array, bits: int) -> np.array:
    """Quantize image with values 0 =< v <= 1 to e.g. 8 bits"""
    high = (1 << bits) - 1
    return (img * high).astype(_type_for_bit_width(bits))


#def downsample(img: np.array, bits: int) -> np.array:
#    return ((img+1) // (256 // (1 << bits))).astype('uint8')


def tile(img: np.array, shape: Tuple[int, int]) -> Sequence[np.array]:
    tile_width, tile_height = shape
    w, h = img.shape[1], img.shape[0]
    width = w // tile_width
    height = h // tile_height
    for y in range(height):
        for x in range(width):
            yield img[tile_height*y:tile_height*(y+1), tile_width*x:tile_width*(x+1)]
