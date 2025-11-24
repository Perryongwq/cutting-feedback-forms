import React from 'react';
import './GridCell.css';

const GridCell = ({ selected, onClick, blockLabel, blockColor, cellNumber }) => {
  const cellStyle = {
    backgroundColor: selected 
      ? (blockColor || '#ff0000') 
      : '#ffffff',
    border: '1px solid #000',
    position: 'relative',
  };

  if (selected && blockColor) {
    cellStyle.opacity = 0.7;
  }

  return (
    <div 
      className={`grid-cell ${selected ? 'selected' : ''}`}
      style={cellStyle}
      onClick={onClick}
    >
      <span className="grid-cell-number">{cellNumber}</span>
      {selected && blockLabel && (
        <span className="grid-cell-label" style={{ color: '#000' }}>
          {blockLabel}
        </span>
      )}
    </div>
  );
};

export default GridCell;

