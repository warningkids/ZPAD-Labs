#include "KeyProcessor.hpp"

void KeyProcessor::processKey(int key) {
    if (key == 'i') currentMode = INVERT;
    if (key == 'b') currentMode = BLUR;
    if (key == 'c') currentMode = CANNY;
    if (key == 'n') currentMode = NORMAL;
}
