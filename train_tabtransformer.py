# =====================================
# 1. IMPORT LIBRARIES
# =====================================
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
import time   # 🔥 ADDED

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

print("Loading dataset...")

# ===============================
# LOAD DATASET
# ===============================

data = pd.read_csv(
    '../dataset_placeholder/iot_ids_dataset.csv',
    sep='\t',
    engine='python'
)

data.columns = data.columns.str.strip()
data = data.dropna()

# ===============================
# CHECK ORIGINAL LABELS
# ===============================

print("\nOriginal attack_type values:")
print(data['attack_type'].unique())

print("\nOriginal attack_type distribution:")
print(data['attack_type'].value_counts())

# ===============================
# CONVERT LABELS TO BINARY
# ===============================

data['attack_type'] = data['attack_type'].astype(str).str.strip().str.upper()

data['attack_type'] = data['attack_type'].apply(
    lambda x: 0 if x == "NORMAL" else 1
)

print("\nBinary attack_type distribution:")
print(data['attack_type'].value_counts())

# ===============================
# ENCODE CATEGORICAL FEATURES
# ===============================

for col in data.select_dtypes(include=['object']).columns:
    if col != 'attack_type':
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col].astype(str))

# ===============================
# FEATURE / LABEL SPLIT
# ===============================

X = data.drop('attack_type', axis=1)
y = data['attack_type']

# ===============================
# NORMALIZE FEATURES
# ===============================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ===============================
# TRAIN TEST SPLIT
# ===============================

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42
)

# ===============================
# BUILD MODEL
# ===============================

print("\nBuilding TinyML compatible model...")

model = keras.Sequential([
    keras.layers.Dense(16, activation='relu', input_shape=(X_train.shape[1],)),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# ===============================
# TRAIN MODEL
# ===============================

print("\nTraining model...")

model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=256,
    validation_split=0.2
)

# ===============================
# EVALUATE MODEL
# ===============================

loss, accuracy = model.evaluate(X_test, y_test)

print("\nModel Accuracy:", accuracy)

# ===============================
# 🔥 MEASURE EXECUTION TIME
# ===============================

print("\nMeasuring execution time...")

start_time = time.time()

predictions_prob = model.predict(X_scaled)

end_time = time.time()

execution_time = end_time - start_time

print("\nExecution Time:", execution_time, "seconds")

# ===============================
# PREDICT FULL DATASET
# ===============================

predictions = (predictions_prob > 0.5).astype(int)

attack_packets = int((predictions == 1).sum())
normal_packets = int((predictions == 0).sum())

total_packets = len(predictions)

attack_percentage = (attack_packets / total_packets) * 100
# ===============================
# EVALUATE MODEL (ADD THIS)
# ===============================
loss, accuracy = model.evaluate(X_test, y_test)

print("\nModel Accuracy:", accuracy)
print("\n==============================")
print("FINAL RESULT:")
print("==============================")
print("Total packets analyzed:", total_packets)
print("Attack packets detected:", attack_packets)
print("Normal packets detected:", normal_packets)
print("Attack Percentage: {:.2f}%".format(attack_percentage))

if attack_packets > 0:
    print("\n⚠ DDoS Attack Detected in the Network")
else:
    print("\n✓ Network Traffic is Normal")

# ===============================
# SAVE MODEL
# ===============================

model.save("tabtransformer_model.keras")

print("\nModel saved successfully!")