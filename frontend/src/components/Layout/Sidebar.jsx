import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  const location = useLocation();

  const menuItems = [
    { path: '/a1', label: 'A1 Cutting Process FB', formNo: 'GE9106JO1701-00/10 / Appendix 7.17' },
    { path: '/ghm', label: 'GHM Cutting FB', formNo: 'GE9106JH1701-00/11' },
    { path: '/kem', label: 'KEM Cutting FB', formNo: '' },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>Cutting Feedback</h2>
      </div>
      <nav className="sidebar-nav">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path || 
                          (item.path === '/a1' && location.pathname === '/');
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`sidebar-item ${isActive ? 'active' : ''}`}
            >
              <div className="sidebar-item-label">{item.label}</div>
              {item.formNo && (
                <div className="sidebar-item-formno">{item.formNo}</div>
              )}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
};

export default Sidebar;

