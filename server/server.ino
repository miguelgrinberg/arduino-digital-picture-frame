// comment the following line if you are not using an Arduino Esplora board
#define IS_ESPLORA

#include <TFT.h>
#include <SPI.h>

#ifdef IS_ESPLORA
#define display EsploraTFT
#else

// the following pins are for the Arduino Uno, change if necessary
#define CS 10
#define DC 9
#define RESET 8 
TFT display = TFT(CS, DC, RESET);

#endif

unsigned short *line = 0;

void setup()
{
    display.begin();
    display.background(0,0,0);
    Serial.begin(115200);
    line = new unsigned short[display.width()];
}

void loop() {
    int bytes;
    if (Serial.available() > 0) {
        char cmd = Serial.read();
        switch (cmd) {
        case 'C': // connect
            Serial.println(display.width());
            Serial.println(display.height());
            break;
        case 'I': // image
            for (int row = 0; row < display.height(); row++) {
                bytes = display.width() * 2;
                char* p = (char*)line;
                while (bytes > 0) {
                    int n = Serial.readBytes(p, bytes);
                    if (n == 0) {
                        // timeout
                        return;
                    }
                    p += n;
                    bytes -= n;
                }
                for (int col = 0; col < display.width(); col++)
                    display.drawPixel(col, row, line[col]);
            }
        }
    }
}

