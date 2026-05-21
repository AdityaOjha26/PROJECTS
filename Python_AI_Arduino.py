import serial
import time
import collections
import pandas as pd
from sklearn.linear_model import LinearRegression

SERIAL_PORT = 'COM8'  
BAUD_RATE = 9600
AI_THRESHOLD = 27.0  

recent_temperatures = collections.deque(maxlen=3)

X_train = []
y_train = []

print("Initializing AI Thermal Hub...")
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) 
    print(f"Successfully connected to {SERIAL_PORT}!")
except Exception as e:
    print(f"Error connecting to port: {e}")
    exit()


ai_model = LinearRegression()
model_trained = False

print("\nWaiting for steady sensor data stream... (Need at least 4 readings to start AI)")

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8',errors='ignore').strip()
            try:
                temp_str, hum_str = line.split(',')
                current_temp = float(temp_str)
                current_hum = float(hum_str)
            except ValueError:
                continue

            print(f"\n[Hardware Input] Temp: {current_temp}°C | Humidity: {current_hum}%")

            if model_trained and len(recent_temperatures) == 3:
                
                features = [list(recent_temperatures)]
                predicted_next_temp = ai_model.predict(features)[0]
                
                print(f"[AI Forecast] Predicted Temp in 6s: {predicted_next_temp:.2f}°C")
                
                if predicted_next_temp >= AI_THRESHOLD and current_temp < AI_THRESHOLD:
                    print("⚠️ [AI ALERT] Thermal anomaly detected! Temperature rising fast.")
                elif current_temp >= AI_THRESHOLD:
                    print("🚨 [HARDWARE ALERT] Threshold crossed. Local safety loop active.")

            if len(recent_temperatures) == 3:
               
                X_train.append(list(recent_temperatures))
                y_train.append(current_temp)
            
                if len(X_train) >= 5:
                    ai_model.fit(X_train, y_train)
                    model_trained = True
                    
            recent_temperatures.append(current_temp)

    except KeyboardInterrupt:
        print("\nStopping AI Hub...")
        ser.close()
        break
