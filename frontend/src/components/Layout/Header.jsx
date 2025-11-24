import React from 'react';
import { useLocation } from 'react-router-dom';
import './Header.css';

const Header = () => {
  const location = useLocation();

  const getTitle = () => {
    if (location.pathname === '/a1' || location.pathname === '/') {
      return 'A1 cutting process feedback system';
    } else if (location.pathname === '/ghm') {
      return 'GHM cutting process feedback system';
    } else if (location.pathname === '/kem') {
      return 'B1 KEM cutting process feedback system';
    }
    return 'Cutting Process Feedback';
  };

  return (
    <header className="header">
      <h1 className="header-title">{getTitle()}</h1>
    </header>
  );
};

export default Header;

