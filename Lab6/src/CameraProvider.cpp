#include "CameraProvider.hpp"
#include <iostream>

CameraProvider::CameraProvider() {
    cap.open(0, cv::CAP_V4L2);

    if (!cap.isOpened()) {
        std::cout << "Cannot open camera!" << std::endl;
    } else {
        std::cout << "Camera opened successfully!" << std::endl;
    }

    cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);
    cap.set(cv::CAP_PROP_FOURCC, cv::VideoWriter::fourcc('M','J','P','G'));
}
cv::Mat CameraProvider::getFrame() {
    cv::Mat frame;
    cap >> frame;
    return frame;
}
