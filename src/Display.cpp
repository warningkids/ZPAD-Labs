#include "Display.hpp"

Display::Display() {
    cv::namedWindow(windowName, cv::WINDOW_NORMAL);
}

void Display::show(const cv::Mat& frame) {
    cv::imshow(windowName, frame);
}
