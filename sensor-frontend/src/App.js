import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Papa from 'papaparse'; // Import papaparse
import ClockWidget from './ClockWidget';

function App() {
  const [sensorData, setSensorData] = useState({});
  const [weatherPredictions, setWeatherPredictions] = useState([]);
  const [alertEnabled, setAlertEnabled] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [alertThreshold, setAlertThreshold] = useState(30);
  const [raindropData, setRaindropData] = useState({});
  const [showWeatherPredictions, setShowWeatherPredictions] = useState(false);

  useEffect(() => {
    const fetchSensorData = async () => {
      // Fetch sensor data from Flask backend
      try {
        const response = await axios.get('http://localhost:5000/sensor_data');
        setSensorData(response.data);
      } catch (error) {
        console.error('Error fetching sensor data:', error);
      }
    };

    const fetchWeatherPredictions = async () => {
      // Fetch weather predictions from Flask backend
      try {
        const response = await axios.get('http://localhost:5000/weather_predictions_selected');
        
        // Parse the CSV data using papaparse
        const parsedData = Papa.parse(response.data, { header: true }).data;

        // Filter out empty objects
        const filteredData = parsedData.filter(item => Object.keys(item).length > 0);

        const filteredDataNew = filteredData.pop()

        console.log('Filtered response from backend:', filteredDataNew);
        setWeatherPredictions(filteredData);
      } catch (error) {
        console.error('Error fetching weather predictions:', error);
      }
    };

    fetchSensorData();
    fetchWeatherPredictions();
    
    const intervalId = setInterval(fetchSensorData, 1000);

    return () => clearInterval(intervalId);
    
  }, []);

    useEffect(() => {
    // ... Fetching sensor data and weather predictions ...

    // Fetch soil moisture data from Flask backend
    const fetchSoilMoisture = async () => {
      try {
        const response = await axios.get('http://localhost:5000/soil_moisture');
        setSensorData(prevData => ({ ...prevData, moisture: response.data.moisture }));
        //~ console.log('Moisture Value:', response.data.moisture);
        console.log('Moisture Value after state update:', sensorData.moisture);
      } catch (error) {
        console.error('Error fetching soil moisture data:', error);
      }
    };
    
    fetchSoilMoisture();
    
    // Fetch data periodically
    const intervalId = setInterval(fetchSoilMoisture, 1000);

    return () => clearInterval(intervalId);
  }, [sensorData.moisture]);

  useEffect(() => {
      const fetchRaindropData = async () => {
          try {
              const response = await axios.get('http://localhost:5000/raindrop_sensor');
              setSensorData(prevData => ({ ...prevData, rain_detected: response.data.rain_detected }));
              console.log('Rainfall Value after state update:', sensorData.rain_detected);
          } catch (error) {
              console.error('Error fetching raindrop sensor data:', error);
          }
      };

      fetchRaindropData();

      const intervalId = setInterval(fetchRaindropData, 1000);

      return () => clearInterval(intervalId);
  }, [sensorData.rain_detected]);
  
  useEffect(() => {
    if (alertEnabled && sensorData.temperature > alertThreshold) {
      //window.alert(`Temperature alert: Temperature is above ${alertThreshold}°C!`);
    }
  }, [sensorData.temperature, alertEnabled, alertThreshold]);

  const handleAlertToggle = () => {
    setAlertEnabled(!alertEnabled);
  };
  
  const toggleWeatherPredictions = () => {
    setShowWeatherPredictions(!showWeatherPredictions);
  };
  
  const handleSidebarToggle = () => {
    setSidebarOpen(!sidebarOpen); // Toggle sidebar state
  };

  return (
      
      <div className="App">      
      <div className="sidebar">
      <div className="slider-container">
      <h2>Alert Settings</h2>
      <label>Temperature Alert Threshold: {alertThreshold}°C</label>
      <input
        type="range"
        min="0"
        max="50"
        step="1"
        value={alertThreshold}
        onChange={event => setAlertThreshold(event.target.value)}
      />
      <label className="switch">
		<input type="checkbox" onChange={handleAlertToggle} style={{ transform: 'scale(1.5)' }} />
		<span className="slider round"></span>
	  </label>
      </div>
      </div>
      
      <div className={`content ${alertEnabled && sensorData.temperature > alertThreshold ? 'has-alert' : ''}`}>
        <div className={`alert-popup ${alertEnabled && sensorData.temperature > alertThreshold ? 'active' : ''}`}>
          <p>Temperature alert: Temperature is above {alertThreshold}°C!</p>
        </div>

        <h1>Sensor Data and Weather Predictions</h1>
      <ClockWidget />
      <div className="container">
          
          <div className="card">
            <h2>Temperature</h2>
            <p>{sensorData.temperature || 'Loading...'} °C</p>
          </div>
          <div className="card">
            <h2>Humidity</h2>
            <p>{sensorData.humidity || 'Loading...'} %</p>
          </div>
          <div className="card">
            <h2>Pressure</h2>
            <p>{sensorData.pressure || 'Loading...'} hPa</p>
          </div>
          <div className="card">
            <h2>Gas Resistance</h2>
            <p>{sensorData.gas || 'Loading...'} Ohms</p>
          </div>
          <div className="card">
            <h2>Soil Moisture</h2>
            <p>{sensorData.moisture === 1 ? 'Dry' : 'Moist'}</p>
          </div>
          <div className="card">
            <h2>Raindrop Sensor</h2>
            <p>{sensorData.rain_detected === 1 ? 'Rain not Detected' : 'Rain Detected'}</p>
          </div>
          
      </div>
      
      <br></br>
      
      <div className="containerForWeather">
        <div className="weather-predictions">
          <h2 onClick={toggleWeatherPredictions}>Predict Weather</h2>
          {showWeatherPredictions && (
            <ul>
              {weatherPredictions.map((prediction, index) => (
                <li key={index}>
                  Date: {prediction.ds}<br />
                  Average Temperature: {prediction.trend}<br />
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>

    </div>
      
    
  );
}

export default App;




