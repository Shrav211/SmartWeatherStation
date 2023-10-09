from flask import Flask, render_template, jsonify
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

app = Flask(__name__)

# Load the CSV data and store it in the `data` variable
data = []
data_lock = threading.Lock()

def load_data_from_csv(file_path):
    global data  # Specify 'data' as a global variable
    with data_lock:
        data.clear()
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # Skip the header row
            for row in csv_reader:
                data.append([float(value) if idx != 0 else value for idx, value in enumerate(row)])
        data = np.array(data)

def save_data_to_csv(file_path, new_row):
    global data  # Specify 'data' as a global variable
    with data_lock:
        with open(file_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(new_row)

# Load the CSV data when the Flask application starts
load_data_from_csv('sensor_data_new.csv')  # Make sure the CSV file is in the correct location

# Load the trained Random Forest model
model = joblib.load('model.pkl')  # Make sure the model file is in the correct location

def predict_temperature_spikes(features):
    prediction = model.predict([features])
    return prediction[0]

@app.route('/')
def index():
    # Load the last row of data from the CSV file (data[-1])
    last_row = data[-1]
    
    # Extract the features for prediction (excluding the first column)
    prediction_features = last_row[2:]
    
    # Predict temperature spike using the trained Random Forest model
    predicted_temperature = predict_temperature_spikes(prediction_features)

    return render_template('index.html', predicted_temperature=predicted_temperature)

@app.route('/save_data', methods=['POST'])
def save_data():
    # Assuming you have access to the new row of data to be saved (e.g., through a POST request)
    new_row = [timestamp, temperature, humidity, pressure, gas]  # Replace with your new data
    save_data_to_csv('sensor_data.csv', new_row)
    return 'Data saved successfully'

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True)
