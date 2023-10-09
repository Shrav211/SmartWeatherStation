from flask import Flask, render_template
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import csv
import threading
import time

app = Flask(__name__)

model = joblib.load('model.pkl') 

def load_data_from_csv(file_path):
    global data, header  # Specify 'data' and 'header' as global variables
    with data_lock:
        data.clear()
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # Save the header separately
            for row in csv_reader:
                data.append([float(value) if idx != 0 else value for idx, value in enumerate(row)])
        data = np.array(data)

def save_data_to_csv(file_path, new_row):
    with data_lock:
        with open(file_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(new_row)

    # After saving data, update the 'data' variable with the new row
    data.append(new_row)

# Load the CSV data and store it in the `data` variable
data = []
header = []
data_lock = threading.Lock()
load_data_from_csv('sensor_data.csv')  # Make sure the CSV file is in the correct location

def train_model_thread():
    global model, data, header
    while True:
        # Load the CSV data when training the model
        load_data_from_csv('sensor_data.csv')  # Make sure the CSV file is in the correct location

        # Extract features and target variable from the loaded data
        features = data[:, 2:]  # Exclude the timestamp and temperature columns
        target = data[:, 1]  # Use the second column (temperature) as the target

        # Train the Random Forest model on the data
        model = RandomForestRegressor()
        model.fit(features, target)

        # Save the trained model
        joblib.dump(model, 'model.pkl')  # Make sure to create the model.pkl file

        # Sleep for 2 minutes before training again
        time.sleep(120)

# Start the training thread
training_thread = threading.Thread(target=train_model_thread)
training_thread.start()

def predict_temperature_spikes(features):
    prediction = model.predict([features])
    return prediction[0]

@app.route('/')
def index():
    with data_lock:
        # Load the last row of data from the CSV file (data[-1])
        last_row = data[-1]

    # Extract the values from the last row
    timestamp, temperature, humidity, pressure, gas = last_row

    # Extract the features for prediction (excluding the timestamp)
    prediction_features = last_row[2:]

    # Predict temperature spike using the trained Random Forest model
    predicted_temperature = predict_temperature_spikes(prediction_features)

    return render_template('index.html', timestamp=timestamp, temperature=temperature,
                           humidity=humidity, pressure=pressure, gas=gas,
                           predicted_temperature=predicted_temperature)

@app.route('/save_data', methods=['POST'])
def save_data():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Assuming you have access to the new row of data to be saved (e.g., through a POST request)
    new_row = [timestamp, temperature, humidity, pressure, gas]  # Replace with your new data

    # Save the data to the CSV file and update 'data' with the new row
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
