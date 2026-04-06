#pragma once
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>

class FaceDetector {
private:
    cv::dnn::Net net;

    std::thread worker;
    std::mutex mtx;
    std::atomic<bool> running{false};

    cv::Mat frame;
    std::vector<cv::Rect> faces;

public:
    FaceDetector();
    ~FaceDetector();

    void start();
    void stop();

    void setFrame(const cv::Mat& newFrame);
    std::vector<cv::Rect> getFaces();

private:
    void process();
};
