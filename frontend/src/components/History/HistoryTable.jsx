import React, { useState, useMemo } from 'react';
import './HistoryTable.css';

const HistoryTable = ({ data, columns }) => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [filterText, setFilterText] = useState('');

  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const sortedAndFilteredData = useMemo(() => {
    let result = [...data];

    // Apply filter
    if (filterText) {
      result = result.filter((row) =>
        Object.values(row).some((value) =>
          String(value).toLowerCase().includes(filterText.toLowerCase())
        )
      );
    }

    // Apply sort
    if (sortConfig.key) {
      result.sort((a, b) => {
        const aVal = a[sortConfig.key] || '';
        const bVal = b[sortConfig.key] || '';
        
        if (sortConfig.direction === 'asc') {
          return String(aVal).localeCompare(String(bVal));
        } else {
          return String(bVal).localeCompare(String(aVal));
        }
      });
    }

    return result;
  }, [data, sortConfig, filterText]);

  if (!data || data.length === 0) {
    return <div className="history-table-empty">No history data available</div>;
  }

  const displayColumns = columns || Object.keys(data[0] || {});

  return (
    <div className="history-table-container">
      <div className="history-table-filter">
        <input
          type="text"
          placeholder="Search history..."
          value={filterText}
          onChange={(e) => setFilterText(e.target.value)}
          className="history-table-search"
        />
      </div>
      <div className="history-table-wrapper">
        <table className="history-table">
          <thead>
            <tr>
              {displayColumns.map((column) => (
                <th
                  key={column}
                  onClick={() => handleSort(column)}
                  className="history-table-header"
                >
                  {column}
                  {sortConfig.key === column && (
                    <span className="history-table-sort-indicator">
                      {sortConfig.direction === 'asc' ? ' ↑' : ' ↓'}
                    </span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sortedAndFilteredData.map((row, index) => (
              <tr key={index}>
                {displayColumns.map((column) => (
                  <td key={column} className="history-table-cell">
                    {row[column] || ''}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="history-table-info">
        Showing {sortedAndFilteredData.length} of {data.length} records
      </div>
    </div>
  );
};

export default HistoryTable;


