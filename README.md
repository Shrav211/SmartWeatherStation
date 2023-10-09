# SmartWeatherStation

## Research Topic
The Smart Weather Station is an IoT device that uses Edge Computing and TinyML to optimize the performance of Machine Learning algorithms for real-time data processing. This device is designed to collect weather data, such as temperature, humidity, and air pressure, and analyze it to provide accurate weather forecasts and alerts.

## Designs & Technical Implementation
* The Smart Weather Station will be designed to be compact and easy to install, with a user-friendly interface for data visualization and analysis 
* The device will use Edge Computing and TinyML to optimize the performance of Machine Learning algorithms for real-time data processing.
* The device will be equipped with sensors to collect weather data and a microcontroller to process and analyze the data.

## Objectives
* To combine cutting-edge sensor technology with machine learning to provide real-time environmental monitoring. 

* To help users track temperature, humidity, pressure, gas levels, soil moisture, and rain detection all in one place. 

* To create a smart alert system that notifies users when specific conditions, like high temperature, are detected.

* Predict future parameters by using a Machine Learning Model.

* Automatically water plants based on the temperature and soil moisture content

## Technologies Used
Flask and React constitute a dynamic web stack with Flask handling the backend using Python and React powering the frontend with interactive interfaces.

When coupled with IoT and Raspberry Pi, everyday objects can be connected to the internet for data exchange.

Integrating Edge Computing and TinyML enables running lightweight AI models on devices like Raspberry Pi, enhancing real-time processing and privacy.

This synergy facilitates applications such as smart homes, environmental monitoring, and industrial automation, blending digital and physical realms seamlessly.

Integrating Edge Computing and TinyML into Internet of Things (IoT) devices and smart sensors enables these devices to perform local data processing and decision-making without relying on constant cloud connectivity. 

This reduces latency and bandwidth usage, making them more responsive and efficient. 

These devices can analyze sensor data, detect anomalies, and trigger actions based on local intelligence.

## Hardware Components
- BME680
  - Temperature Sensor
  - Humidity Sensor
  - Air Pressure Sensor 
  - Gas Resistance Sensor 

- Soil Moisture Sensor   FC-28 

- Rainfall Sensor   SEN-3115

- Raspberry Pi 4 

## Software Components
- Flask Framework as a Backend for our Web Application

- React as a Frontend for our Web Application 

- AI model
  - Prophet ( Time Series Model ) 
