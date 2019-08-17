#!/usr/bin/python
## for python3.6
import glob
import os
import sys
import functools

from PIL import Image

EXTS = 'jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG'

reduce = functools.reduce

def avhash(im):
    if not isinstance(im, Image.Image):
        print(f"im: {im}")
        im = Image.open(im)
    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64.
    return reduce(lambda x, yz: x | (yz[-1] << yz[0]),enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),0)

def hamming(h1, h2):
    print(f"h1:{h1}, h2:{h2}")
    h, d = 0, h1 ^ h2
    print(f"d: {d}")
    while d:
        h += 1
        d &= d - 1
    return h

def process(img, imgs_dir):
        print(img, imgs_dir)
        im = img
        wd = imgs_dir
        h = avhash(im)
        print(os.getcwd())
        os.chdir(wd)
        print(os.getcwd())
        images = []
        for ext in EXTS:
            images.extend(glob.glob(f'*.{ext}'))

        seq = []
        prog = int(len(images) > 50 and sys.stdout.isatty())
        for f in images:
            seq.append((f, hamming(avhash(f), h)))
            if prog:
                perc = 100. * prog / len(images)
                x = int(2 * perc / 5)
                print(f"\rCalculating... [{'#' * x} {' ' * (40 - x)} ]", end='')
                print(f"{perc:.2f}% {prog}/{len(images)}", end='')
                sys.stdout.flush()
                prog += 1
            break

        if prog: print
        for f, ham in sorted(seq, key=lambda i: i[1]):
            print(f"{ham}\t{f}")

                      
if 0 and __name__ == '__main__':
    if len(sys.argv) <= 1 or len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} image.jpg [dir]")
    else:
        im, wd = sys.argv[1], '.' if len(sys.argv) < 3 else sys.argv[2]
        process(im, wd)

