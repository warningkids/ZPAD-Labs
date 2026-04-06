#pragma once

class KeyProcessor {
public:
    enum Mode {
        NORMAL,
        INVERT,
        BLUR,
        CANNY,
        FACE
    };

    Mode currentMode = NORMAL;

    void processKey(int key);
};
