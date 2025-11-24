import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import './DateTimePicker.css';

const DateTimePicker = ({ value, onChange, error, label }) => {
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');

  useEffect(() => {
    if (value) {
      try {
        const dateTime = new Date(value);
        setDate(format(dateTime, 'yyyy-MM-dd'));
        setTime(format(dateTime, 'HH:mm:ss'));
      } catch (e) {
        // If value is already in format 'YYYY-MM-DD HH:MM:SS'
        const parts = value.split(' ');
        if (parts.length === 2) {
          setDate(parts[0]);
          setTime(parts[1]);
        }
      }
    } else {
      // Default to current date/time
      const now = new Date();
      setDate(format(now, 'yyyy-MM-dd'));
      setTime(format(now, 'HH:mm:ss'));
      onChange(`${format(now, 'yyyy-MM-dd')} ${format(now, 'HH:mm:ss')}`);
    }
  }, []);

  const handleDateChange = (e) => {
    const newDate = e.target.value;
    setDate(newDate);
    if (time) {
      onChange(`${newDate} ${time}`);
    }
  };

  const handleTimeChange = (e) => {
    const newTime = e.target.value;
    setTime(newTime);
    if (date) {
      onChange(`${date} ${newTime}`);
    }
  };

  return (
    <div className="datetime-picker">
      {label && <label className="datetime-picker-label">{label}</label>}
      <div className="datetime-picker-inputs">
        <input
          type="date"
          value={date}
          onChange={handleDateChange}
          className={`datetime-picker-date ${error ? 'error' : ''}`}
        />
        <input
          type="time"
          value={time}
          onChange={handleTimeChange}
          step="1"
          className={`datetime-picker-time ${error ? 'error' : ''}`}
        />
      </div>
      {error && <div className="datetime-picker-error">{error}</div>}
    </div>
  );
};

export default DateTimePicker;

