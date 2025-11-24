import React, { useState, useRef, useEffect } from 'react';
import './MultiSelect.css';

const MultiSelect = ({ options, value = [], onChange, placeholder = 'Select...', error, label }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const toggleOption = (option) => {
    const newValue = value.includes(option)
      ? value.filter((v) => v !== option)
      : [...value, option];
    onChange(newValue);
  };

  const removeOption = (option, e) => {
    e.stopPropagation();
    onChange(value.filter((v) => v !== option));
  };

  return (
    <div className="multiselect">
      {label && <label className="multiselect-label">{label}</label>}
      <div
        ref={dropdownRef}
        className={`multiselect-dropdown ${isOpen ? 'open' : ''} ${error ? 'error' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="multiselect-selected">
          {value.length === 0 ? (
            <span className="multiselect-placeholder">{placeholder}</span>
          ) : (
            <div className="multiselect-tags">
              {value.map((option) => (
                <span key={option} className="multiselect-tag">
                  {option}
                  <button
                    type="button"
                    className="multiselect-tag-remove"
                    onClick={(e) => removeOption(option, e)}
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}
          <span className="multiselect-arrow">▼</span>
        </div>
        {isOpen && (
          <div className="multiselect-options">
            {options.map((option) => (
              <div
                key={option}
                className={`multiselect-option ${value.includes(option) ? 'selected' : ''}`}
                onClick={() => toggleOption(option)}
              >
                <input
                  type="checkbox"
                  checked={value.includes(option)}
                  onChange={() => toggleOption(option)}
                  readOnly
                />
                <span>{option}</span>
              </div>
            ))}
          </div>
        )}
      </div>
      {error && <div className="multiselect-error">{error}</div>}
    </div>
  );
};

export default MultiSelect;


