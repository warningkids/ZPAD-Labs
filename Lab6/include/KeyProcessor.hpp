#pragma once

class KeyProcessor {
public:
    enum Mode {
        NORMAL,
        INVERT,
        BLUR,
        CANNY
    };

    Mode currentMode = NORMAL;

    void processKey(int key);
};
