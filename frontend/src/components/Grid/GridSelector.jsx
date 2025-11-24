import React, { useState, useEffect } from 'react';
import GridCell from './GridCell';
import './GridSelector.css';

const GridSelector = ({ 
  size = 6, // 6x6 for A1, 3x3 for GHM/KEM
  value = null, 
  onChange, 
  showBlockLabels = false, // Show A, B, C, D labels for A1
  label = '' 
}) => {
  // Initialize grid state
  const initializeGrid = () => {
    if (value && Array.isArray(value) && value.length === size) {
      return value.map(row => [...row]);
    }
    return Array(size).fill(null).map(() => Array(size).fill(false));
  };

  const [grid, setGrid] = useState(initializeGrid);

  useEffect(() => {
    if (value) {
      setGrid(value.map(row => [...row]));
    }
  }, [value]);

  const toggleCell = (row, col) => {
    const newGrid = grid.map(r => [...r]);
    newGrid[row][col] = !newGrid[row][col];
    setGrid(newGrid);
    if (onChange) {
      onChange(newGrid);
    }
  };

  const selectAll = () => {
    const newGrid = Array(size).fill(null).map(() => Array(size).fill(true));
    setGrid(newGrid);
    if (onChange) {
      onChange(newGrid);
    }
  };

  const deselectAll = () => {
    const newGrid = Array(size).fill(null).map(() => Array(size).fill(false));
    setGrid(newGrid);
    if (onChange) {
      onChange(newGrid);
    }
  };

  const getBlockLabel = (row, col) => {
    if (!showBlockLabels || size !== 6) return null;
    
    // A1 grid layout:
    // Rows 0-2: Blocks A (left 3) and B (right 3)
    // Rows 3-5: Blocks C (left 3) and D (right 3)
    if (row < 3) {
      return col < 3 ? 'A' : 'B';
    } else {
      return col < 3 ? 'C' : 'D';
    }
  };

  const getBlockColor = (row, col) => {
    if (!showBlockLabels || size !== 6) return null;
    
    const block = getBlockLabel(row, col);
    const colors = {
      'A': '#ff0000', // Red
      'B': '#00ff00', // Green
      'C': '#0000ff', // Blue
      'D': '#fff000'  // Yellow
    };
    return colors[block] || null;
  };

  return (
    <div className="grid-selector">
      {label && <div className="grid-selector-label">{label}</div>}
      <div className="grid-selector-controls">
        <button type="button" className="btn btn-secondary" onClick={selectAll}>
          Select All
        </button>
        <button type="button" className="btn btn-secondary" onClick={deselectAll}>
          Deselect All
        </button>
      </div>
      <div className="grid-selector-grid" style={{ gridTemplateColumns: `repeat(${size}, 1fr)` }}>
        {grid.map((row, rowIndex) =>
          row.map((cell, colIndex) => (
            <GridCell
              key={`${rowIndex}-${colIndex}`}
              selected={cell}
              onClick={() => toggleCell(rowIndex, colIndex)}
              blockLabel={getBlockLabel(rowIndex, colIndex)}
              blockColor={getBlockColor(rowIndex, colIndex)}
              cellNumber={rowIndex * size + colIndex + 1}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default GridSelector;

