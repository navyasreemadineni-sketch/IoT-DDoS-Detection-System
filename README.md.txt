
Lightweight Embedded DDoS Detection using TinyML on ESP32
==========================================================

This project demonstrates a simple pipeline:
1. Train a lightweight ML model for DDoS detection.
2. Convert the model to TensorFlow Lite Micro format.
3. Deploy the model on ESP32 using Arduino.

Folder Structure:
- dataset_placeholder/ : Place your IoT IDS dataset CSV here.
- ml_training/         : Python code for training ML model.
- tinyml_conversion/   : Convert trained model to TFLite Micro.
- esp32_firmware/      : Arduino code for ESP32 deployment.

Requirements:
Python libraries:
- pandas
- numpy
- scikit-learn
- tensorflow

Hardware:
- ESP32 Dev Board

Steps:
1. Put dataset CSV inside dataset_placeholder folder.
2. Run ml_training/train_model.py
3. Run tinyml_conversion/convert_to_tflite.py
4. Copy generated model.h into esp32_firmware folder.
5. Open esp32_firmware/esp32_ddos_detector.ino in Arduino IDE and upload.

