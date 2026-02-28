#include "FrameProcessor.hpp"

cv::Mat FrameProcessor::process(const cv::Mat& frame, KeyProcessor::Mode mode) {
    cv::Mat result = frame.clone();

    switch (mode) {
        case KeyProcessor::INVERT:
            cv::bitwise_not(frame, result);
            break;

        case KeyProcessor::BLUR:
            cv::GaussianBlur(frame, result, cv::Size(15,15), 0);
            break;

        case KeyProcessor::CANNY:
            cv::Canny(frame, result, 100, 200);
            break;

        default:
            break;
    }

    return result;
}
