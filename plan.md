# Plan

## Hardware limitations

Use 4x8=32 8x16 sprites yielding a total of 64x64 pixels. Each
pixel being 4 bit.

## Rendering

Software render a fixed set of angles (x or x+y), controllable with
contorller. Each angle has a lookup table for each 32 tiles.

## Optimizing tiles

To find out what tile index to use per angle.

1. Render a single angle (e.g. 0)
2. For all other angles - Find the tile that produces the smallest error

## TODO

- Render to 4-bits
- Create lookup tables
- Render .chr file
- Perspective rendering

### Assembler

- Draw tiles in correct positions
- Control angle with controller
- Tweak palette

## Done

✔ Software renderer
