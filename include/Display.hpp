#pragma once
#include <opencv2/opencv.hpp>

class Display {
public:
    Display();
    void show(const cv::Mat& frame);
private:
    std::string windowName = "Lab6 Camera";
};
