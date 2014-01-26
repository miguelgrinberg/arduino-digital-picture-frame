#!/usr/bin/env python
import os
import sys
from serial import Serial
import random
import time
from argparse import ArgumentParser
from PIL import Image

def scan_for_images(folder):
    """Find all the jpg images in a directory tree."""
    return [os.path.join(path, filename)
            for path, dirs, files in os.walk(folder)
            for filename in files
            if filename.endswith(".jpg")]

def upload_image(filename, serial, screen_size):
    """Upload an image to the Arduino digital picture frame server."""
    img = Image.open(filename)
    img.thumbnail(screen_size, Image.ANTIALIAS)
    img_data = img.getdata()

    # center image on display
    top_margin = (screen_size[1] - img.size[1]) / 2
    bottom_margin = screen_size[1] - img.size[1] - top_margin
    left_margin = (screen_size[0] - img.size[0]) / 2
    right_margin = screen_size[0] - img.size[0] - left_margin

    # send image data over serial port
    serial.write('I') # indicate that image data follows
    for row in range(top_margin):
        for col in range(screen_size[0]):
            serial.write('\x00\x00')
    i = 0
    for row in range(img.size[1]):
        for col in range(left_margin):
            serial.write('\x00\x00')
        for col in range(img.size[0]):
            red = img_data[i][0] >> 3
            green = img_data[i][1] >> 2
            blue = img_data[i][2] >> 3
            serial.write('%c%c' % ((((green & 0x03) << 5) | red), (blue << 3) | (green >> 3)))
            i = i + 1
        for col in range(left_margin):
            serial.write('\x00\x00')
    for row in range(bottom_margin):
        for col in range(screen_size[0]):
            serial.write('\x00\x00')

def parse_arguments():
    parser = ArgumentParser(description='Send pictures to the Arduino based digital picture frame.')
    parser.add_argument('--port', '-P', metavar='PORT', required=True,
                        help='serial port connected to the Arduino board.')
    parser.add_argument('--folder', '-f', metavar='FOLDER', default='.',
                        help='picture folder (default: current directory).')
    parser.add_argument('--interval', '-i', metavar='INTERVAL', default=10,
                        help='interval between pictures (default: 10 seconds).')
    parser.add_argument('--baudrate', '-b', metavar='BPS', default=115200,
                        help='serial port baud rate (default: 115200 seconds).')
    return parser.parse_args()
    
def main():
    args = parse_arguments()

    images = scan_for_images(args.folder)
    if len(images) == 0:
        print('Error: found no jpeg images in "%s".' % args.folder)
        sys.exit(1)
    print('Found %d images.' % len(images))

    serial = Serial(args.port)
    serial.baudrate = args.baudrate
    print('Opened serial port %s.' % serial.name)
    
    print('Interval between pictures is %d seconds.' % args.interval)

    width = 0
    height = 0

    # display random pictures
    while True:
        time.sleep(args.interval)

        if width == 0:
            # connect to the Arduino and obtain screen size
            serial.write('C')
            width = int(serial.readline())
            height = int(serial.readline())
            print('Display is %dx%d.' % (width, height))

        image = random.choice(images)
        print('Uploading "%s"...' % image)
        upload_image(image, serial, (width, height))

if __name__ == '__main__':
    main()
