import numpy as np


def intensity(img: np.array) -> np.array:
    return np.mean(img, axis=-1)


def downsample(img: np.array, bits: int) -> np.array:
    return img / (256 // (1 << bits))
