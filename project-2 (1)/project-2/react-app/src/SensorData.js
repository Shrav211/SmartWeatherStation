import React, { useEffect, useState } from 'react';
import axios from 'axios';

const SensorData = () => {
  const [data, setData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.get('/sensor_data');
      setData(response.data);
    };

    const interval = setInterval(fetchData, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>BME680 Sensor Data</h1>
      <ul>
        <li>Temperature: {data.temperature} °C</li>
        <li>Humidity: {data.humidity} %</li>
        <li>Pressure: {data.pressure} hPa</li>
        <li>Gas Resistance: {data.gas} Ω</li>
      </ul>
    </div>
  );
};

export default SensorData;
