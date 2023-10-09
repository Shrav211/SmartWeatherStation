import numpy as np
from sklearn.ensemble import RandomForestRegressor
import csv

import pickle

data = []
with open('sensor_data_train.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)  # Skip the header row
    for row in csv_reader:
        data.append([float(value) for value in row[1:]])
data = np.array(data)

X = data[:, 1:]  # Features 
y = data[:, 0]  # Target variable 

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

pickle.dump(model, open('model.pkl','wb'))

def predict_temperature_spikes(features):
    prediction = model.predict([features])
    return prediction[0]

    
prediction_features = data[-1, 1:]

#prediction_features = [90.0, 913.25, 760108.3127649898]
	
prediction = predict_temperature_spikes(prediction_features)
print("Predicted temperature spike:", prediction, "degree celsius")

if (prediction > 30):
    print("Proceed with irrigation please, temperature is predicted to rise")
else:
    print("Irrigation not currently needed, temperature is NOT predicted to rise")
