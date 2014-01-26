Arduino Digital Picture Frame
=============================

An Arduino digital picture frame server, with a Python client that sends random pictures to it. See my [Arduino Esplora Digital Picture Frame](http://blog.miguelgrinberg.com/post/fun-with-the-arduino-esplora-a-digital-picture-frame) tutorial for more information.

Installation
------------

The `server.ino` file runs on your Arduino board and waits for a client to send pictures to display. This sketch file is ready to run on the Arduino Esplora board, but can be adapted easily to any other Arduino board. In all cases, the Arduino 160x128 TFT screen is assumed, though other similar screens will probably work as well.

The `client.py` script runs on your computer and communicates with the Arduino board over the serial port. This script finds all the images in a directory tree and then uploads random ones to display at regular intervals. To run this script the `pyserial` and `pillow` packages need to be installed. Use `--help` for usage information.

