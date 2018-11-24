import numpy as np

def write(sprite_sheet: np.array) -> bytes:
    """Writes chr file given sprite sheet"""
    if sprite_sheet.shape[1] < 8:
        raise ValueError('Sprite sheet needs to be at least 8 bytes')

    output = bytearray()
    for t in range(sprite_sheet.shape[0] // 8):
        # write plane 0
        for row in range(8):
            for b in np.packbits(sprite_sheet[t * 8 + row][:8] & 1):
                output.append(b)
        # write plane 1
        for row in range(8):
            for b in np.packbits(sprite_sheet[t * 8 + row][:8] & 2):
                output.append(b)
    return bytes(output)