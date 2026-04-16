
#include <TensorFlowLite.h>
#include "ddos_model.h"

// Dummy input feature array
float input_data[10] = {0};

void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 TinyML DDoS Detector Started");
}

void loop() {
  // Dummy prediction simulation
  float prediction = random(0, 100) / 100.0;

  if (prediction > 0.5) {
    Serial.println("DDoS Attack Detected!");
  } else {
    Serial.println("Normal Traffic");
  }

  delay(2000);
}
