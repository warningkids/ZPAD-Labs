#include "FaceDetector.hpp"
#include <chrono>

FaceDetector::FaceDetector() {
    net = cv::dnn::readNetFromCaffe(
        "deploy.prototxt",
        "res10_300x300_ssd_iter_140000.caffemodel"
    );
}

FaceDetector::~FaceDetector() {
    stop();
}

void FaceDetector::start() {
    running = true;
    worker = std::thread(&FaceDetector::process, this);
}

void FaceDetector::stop() {
    running = false;
    if (worker.joinable())
        worker.join();
}

void FaceDetector::setFrame(const cv::Mat& newFrame) {
    std::lock_guard<std::mutex> lock(mtx);
    frame = newFrame.clone();
}

std::vector<cv::Rect> FaceDetector::getFaces() {
    std::lock_guard<std::mutex> lock(mtx);
    return faces;
}

void FaceDetector::process() {
    while (running) {

        cv::Mat localFrame;

        {
            std::lock_guard<std::mutex> lock(mtx);
            if (frame.empty()) continue;
            localFrame = frame.clone();
        }

        cv::Mat blob = cv::dnn::blobFromImage(
            localFrame, 1.0,
            cv::Size(300, 300),
            cv::Scalar(104, 177, 123)
        );

        net.setInput(blob);
        cv::Mat detections = net.forward();

        std::vector<cv::Rect> detectedFaces;

        float* data = (float*)detections.data;

for (int i = 0; i < detections.size[2]; i++) {

    float conf = data[i * 7 + 2];

    if (conf > 0.5) {
        int x1 = data[i * 7 + 3] * localFrame.cols;
        int y1 = data[i * 7 + 4] * localFrame.rows;
        int x2 = data[i * 7 + 5] * localFrame.cols;
        int y2 = data[i * 7 + 6] * localFrame.rows;

        detectedFaces.emplace_back(x1, y1, x2 - x1, y2 - y1);
    }
}

        {
            std::lock_guard<std::mutex> lock(mtx);
            faces = detectedFaces;
        }

      
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}
