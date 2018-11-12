import numpy as np
import png

def main():
    im = np.zeros((64, 64, 4), 'uint8')
    im[32,32] = (255, 0, 0, 255)
    with open('image.png', 'wb') as f:
        f.write(png.write(im.tobytes(), 64, 64))
    
main()