#include <opencv2/opencv.hpp>
#include <iostream>
#include "CameraProvider.hpp"
#include "FrameProcessor.hpp"
#include "KeyProcessor.hpp"
#include "Display.hpp"

int main() {
    CameraProvider camera;
    FrameProcessor processor;
    KeyProcessor keyProcessor;
    Display display;

    double prevTime = cv::getTickCount();
    double fps = 0.0;

    while (true) {

        // Проверка закрытия окна крестиком
        if (cv::getWindowProperty("Lab6 Camera", cv::WND_PROP_VISIBLE) < 1) {
            break;
        }

        cv::Mat frame = camera.getFrame();

        if (frame.empty()) {
            std::cout << "Frame is empty!" << std::endl;
            continue;
        }

        cv::Mat processed = processor.process(frame, keyProcessor.currentMode);

        // ===== FPS calculation =====
        double currentTime = cv::getTickCount();
        double deltaTime = (currentTime - prevTime) / cv::getTickFrequency();
        fps = 1.0 / deltaTime;
        prevTime = currentTime;

        // ===== Draw FPS on frame =====
        cv::putText(processed,
                    "FPS: " + std::to_string((int)fps),
                    cv::Point(10, 30),
                    cv::FONT_HERSHEY_SIMPLEX,
                    0.8,
                    cv::Scalar(0, 255, 0),
                    2);

        display.show(processed);

        int key = cv::waitKey(30);
        keyProcessor.processKey(key);

        // ESC или q для выхода
        if (key == 27 || key == 'q') {
            break;
        }
    }

    cv::destroyAllWindows();
    return 0;
}
