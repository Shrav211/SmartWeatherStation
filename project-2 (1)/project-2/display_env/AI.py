import numpy as np
from sklearn.ensemble import RandomForestRegressor
import csv

data = []
with open('sensor_data_train.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)  # Skip the header row
    for row in csv_reader:
        data.append([float(value) for value in row[1:]])
data = np.array(data)

X = data[:, :-1]  # Features (all columns except the last one)
y = data[:, 1]  # Target variable (last column)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

def predict_temperature_spikes(features):
    prediction = model.predict([features])
    return prediction[0]
    
features = [25.5, 70.2, 1013.2, 1000.0]

prediction = predict_temperature_spikes(features)
print("Predicted temperature spike:", prediction)
