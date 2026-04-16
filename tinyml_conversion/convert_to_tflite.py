import tensorflow as tf

# Load trained model
model = tf.keras.models.load_model("tabtransformer_model.keras")

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

tflite_model = converter.convert()

# Save TFLite model
with open("tabtransformer_model.tflite", "wb") as f:
    f.write(tflite_model)

print("TFLite model created successfully!")