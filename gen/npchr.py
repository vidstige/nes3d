import numpy as np

def write(f, buf: np.array):
    """Writes chr file given buf image"""
    output = bytearray()
    for t in range(buf.shape[0] // 8):
        # write plane 0
        for row in range(8):
            for b in np.packbits(buf[t * 8 + row] & 1):
                output.append(b)
        # write plane 1
        for row in range(8):
            for b in np.packbits(buf[t * 8 + row] & 2):
                output.append(b)
    f.write(output)