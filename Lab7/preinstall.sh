#!/bin/bash
sudo apt update
sudo apt install libopencv-dev cmake g++ wget -y
echo "Downloading face detection model..."
wget -N https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
wget -N https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel
echo "Preinstall finished successfully!"
