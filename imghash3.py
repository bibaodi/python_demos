#!/usr/bin/python

import glob
import os
import sys
import functools

from PIL import Image

EXTS = 'jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG'

reduce = functools.reduce

def avhash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64.
    return reduce(lambda x, yz: x | (yz[-1] << yz[0]),enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),0)

def hamming(h1, h2):
    h, d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    return h

if __name__ == '__main__':
    if len(sys.argv) <= 1 or len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} image.jpg [dir]")
    else:
        im, wd = sys.argv[1], '.' if len(sys.argv) < 3 else sys.argv[2]
        h = avhash(im)

        os.chdir(wd)
        images = []
        for ext in EXTS:
            images.extend(glob.glob('*.%s' % ext))

        seq = []
        prog = int(len(images) > 50 and sys.stdout.isatty())
        for f in images:
            seq.append((f, hamming(avhash(f), h)))
            if prog:
                perc = 100. * prog / len(images)
                x = int(2 * perc / 5)
                #print '\rCalculating... [' + '#' * x + ' ' * (40 - x) + ']',
                print(f"\rCalculating... [{'#' * x} {' ' * (40 - x)} ]", end='')
                #print '%.2f%%' % perc, '(%d/%d)' % (prog, len(images)),
                print(f"{perc:.2f}% {prog}/{len(images)}", end='')
                sys.stdout.flush()
                prog += 1

        if prog: print
        for f, ham in sorted(seq, key=lambda i: i[1]):
            print(f"{ham}\t{f}")