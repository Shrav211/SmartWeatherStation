// ClockWidget.js

import React, { useState, useEffect } from 'react';

function ClockWidget() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const intervalId = setInterval(() => {
      setTime(new Date());
    }, 1000); // Update every second

    return () => clearInterval(intervalId);
  }, []);

  const options = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZoneName: 'short', // Include time zone name (e.g., IST)
  };

  const formattedTime = time.toLocaleTimeString();
  const formattedDate = time.toLocaleDateString(undefined, options);

  return (
    <div className="clock-widget">
      <p className="time">{formattedTime}</p>
      <p className="date">{formattedDate}</p>
    </div>
  );
}

export default ClockWidget;
