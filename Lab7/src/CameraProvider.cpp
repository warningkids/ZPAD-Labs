#include "CameraProvider.hpp"
#include <iostream>

CameraProvider::CameraProvider() {

    // 1️⃣ Пробуем V4L2 (лучший вариант для Linux)
    if (!cap.open(0, cv::CAP_V4L2)) {
        std::cout << "V4L2 failed, trying default backend..." << std::endl;

        // 2️⃣ fallback — обычное открытие
        if (!cap.open(0)) {
            std::cout << "Cannot open camera!" << std::endl;
            return;
        }
    }

    std::cout << "Camera opened successfully!" << std::endl;

    // 3️⃣ Ставим нормальное разрешение (универсальное)
    cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);

    // 4️⃣ Пробуем MJPG (самый стабильный формат)
    cap.set(cv::CAP_PROP_FOURCC, cv::VideoWriter::fourcc('M','J','P','G'));

    // 5️⃣ Немного прогреем камеру (ВАЖНО)
    cv::Mat tmp;
    for (int i = 0; i < 10; i++) {
        cap >> tmp;
    }
}

cv::Mat CameraProvider::getFrame() {
    cv::Mat frame;
    cap >> frame;

    // Если пусто — пробуем ещё раз
    if (frame.empty()) {
        cap >> frame;
    }

    return frame;
}
