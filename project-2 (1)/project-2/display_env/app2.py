from flask import Flask, render_template, jsonify, send_file
import smbus2
import bme680
import RPi.GPIO as GPIO
import time
import threading
import csv
import joblib
import pickle
import sklearn
import numpy as np
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)
app.static_folder = 'static'
GPIO.setmode(GPIO.BCM)
led_pin = 17
GPIO.setup(led_pin, GPIO.OUT)

# Configure BME680 sensor
i2c_address = 0x77  # BME680 sensor I2C address
bus = smbus2.SMBus(1)
sensor = bme680.BME680(i2c_addr=i2c_address)
sensor.set_temp_offset(0)

soil_moisture_pin = 18  # GPIO pin connected to the soil moisture sensor
GPIO.setup(soil_moisture_pin, GPIO.IN)

raindrop_sensor_pin = 25  # GPIO pin connected to the raindrop sensor
GPIO.setup(raindrop_sensor_pin, GPIO.IN)

csv_file = open('sensor_data_new.csv', 'w')
csv_writer = csv.writer(csv_file)

csv_writer.writerow(['Timestamp', 'Temperature', 'Humidity', 'Pressure', 'Gas'])

def load_data_from_csv(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Skip the header row
        for row in csv_reader:
            # Convert all columns except the first one (timestamp) to float
            data.append([float(value) if idx != 0 else value for idx, value in enumerate(row)])
    data = np.array(data)
    return data

# Load the CSV data and store it in the `data` variable
data = load_data_from_csv('sensor_data.csv')

# Load the trained Random Forest model
model = joblib.load('model.pkl')

def predict_temperature_spikes(features, num_predictions=10):
    predictions = model.predict([features] * num_predictions)
    return predictions

@app.route('/')
def index():
    # Load the last row of data from the CSV file (data[-1])
    last_row = data[-1]

    # Extract the features for prediction (excluding the first column)
    prediction_features = last_row[2:]

    # Predict temperature spikes using the trained Random Forest model
    predicted_temperatures = predict_temperature_spikes(prediction_features, num_predictions=10)

    return render_template('index.html', predicted_temperatures=predicted_temperatures)

@app.route('/sensor_data')
def sensor_data():
    sensor.get_sensor_data()
    temperature = sensor.data.temperature
    humidity = sensor.data.humidity
    pressure = sensor.data.pressure
    gas = sensor.data.gas_resistance
    data = {
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure,
        'gas': gas
    }
    return jsonify(data)

def monitor_sensor_data():
    while True:
        sensor.get_sensor_data()
        temperature = sensor.data.temperature
        humidity = sensor.data.humidity
        pressure = sensor.data.pressure
        gas = sensor.data.gas_resistance

        if temperature > 30 and GPIO.input(soil_moisture_pin) == 1:
            GPIO.output(led_pin, GPIO.HIGH)
        else:
            GPIO.output(led_pin, GPIO.LOW)

        # Save sensor data to CSV
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        csv_writer.writerow([timestamp, temperature, humidity, pressure, gas])
        csv_file.flush()  # Flush data to the file immediately

        time.sleep(3600)

temperature_thread = threading.Thread(target=monitor_sensor_data)
temperature_thread.start()

@app.route('/soil_moisture')
def soil_moisture():
    moisture = GPIO.input(soil_moisture_pin)
    data = {
        'moisture': moisture
    }
    return jsonify(data)

@app.route('/raindrop_sensor')
def raindrop_sensor():
    rain_detected = GPIO.input(raindrop_sensor_pin)
    data = {
        'rain_detected': rain_detected
    }
    return jsonify(data)

@app.route('/weather_predictions_selected')
def weather_predictions_selected():
    # Read the CSV file and extract the last 10 rows
    data = []
    with open('weather_predictions_selected_display.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)[-11:]

    # Create a CSV-formatted string
    csv_string = io.StringIO()
    csv_writer = csv.DictWriter(csv_string, fieldnames=data[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(data)

    # Create a BytesIO object to store the CSV data
    csv_io = io.BytesIO(csv_string.getvalue().encode())

    # Return the CSV data as a file
    return send_file(csv_io,
                     mimetype='text/csv',
                     as_attachment=True,
                     attachment_filename='weather_predictions_selected_display.csv')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
