import serial
import time
import collections
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- CONFIGURATION ---
SERIAL_PORT = 'COM8'  # <-- CHANGE THIS to your Arduino's port!
BAUD_RATE = 9600
AI_THRESHOLD = 27.0   # AI alert trigger threshold

# We use a deque to keep track of the last 3 readings for the AI model input
recent_temperatures = collections.deque(maxlen=3)

# Initialize historical lists to store data for online training
X_train = []
y_train = []

print("Initializing AI Thermal Hub...")
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # Wait for Arduino to reset
    print(f"Successfully connected to {SERIAL_PORT}!")
except Exception as e:
    print(f"Error connecting to port: {e}")
    exit()

# Initialize a simple, fast Linear Regression model
ai_model = LinearRegression()
model_trained = False

print("\nWaiting for steady sensor data stream... (Need at least 4 readings to start AI)")

while True:
    try:
        if ser.in_waiting > 0:
            # Read line from Arduino, decode bytes to string, and strip whitespace
            line = ser.readline().decode('utf-8',errors='ignore').strip()
            
            # Parse the CSV values
            try:
                temp_str, hum_str = line.split(',')
                current_temp = float(temp_str)
                current_hum = float(hum_str)
            except ValueError:
                # Ignores initialization text or incomplete serial packets
                continue

            print(f"\n[Hardware Input] Temp: {current_temp}°C | Humidity: {current_hum}%")

            # --- AI LOGIC: PREDICTION ---
            if model_trained and len(recent_temperatures) == 3:
                # Format current window as features for the model: [[t-2, t-1, t]]
                features = [list(recent_temperatures)]
                predicted_next_temp = ai_model.predict(features)[0]
                
                print(f"[AI Forecast] Predicted Temp in 6s: {predicted_next_temp:.2f}°C")
                
                # Predictive early-warning trigger
                if predicted_next_temp >= AI_THRESHOLD and current_temp < AI_THRESHOLD:
                    print("⚠️ [AI ALERT] Thermal anomaly detected! Temperature rising fast.")
                elif current_temp >= AI_THRESHOLD:
                    print("🚨 [HARDWARE ALERT] Threshold crossed. Local safety loop active.")

            # --- AI LOGIC: TRAINING DATA COLLECTION ---
            if len(recent_temperatures) == 3:
                # If we already have a historical window of 3, the NEW reading 
                # is the perfect future target (y) for those 3 past readings (X).
                X_train.append(list(recent_temperatures))
                y_train.append(current_temp)
                
                # Retrain/update the model dynamically with the updated history
                # This lets the AI adapt to your specific room environment
                if len(X_train) >= 5: # Needs a few samples to solve the regression equation
                    ai_model.fit(X_train, y_train)
                    model_trained = True

            # Append the current temperature to our rolling window
            recent_temperatures.append(current_temp)

    except KeyboardInterrupt:
        print("\nStopping AI Hub...")
        ser.close()
        break
