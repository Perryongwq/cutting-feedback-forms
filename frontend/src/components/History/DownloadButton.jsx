import React, { useState } from 'react';
import { downloadA1History, downloadGHMHistory, downloadKEMHistory } from '../../services/api';
import './DownloadButton.css';

const DownloadButton = ({ formType = 'a1' }) => {
  const [loading, setLoading] = useState(false);

  const handleDownload = async () => {
    setLoading(true);
    try {
      let blob;
      let filename;

      switch (formType.toLowerCase()) {
        case 'a1':
          blob = await downloadA1History();
          filename = 'history_A1.xlsx';
          break;
        case 'ghm':
          blob = await downloadGHMHistory();
          filename = 'history_GHM.xlsx';
          break;
        case 'kem':
          blob = await downloadKEMHistory();
          filename = 'history_KEM.xlsx';
          break;
        default:
          throw new Error('Invalid form type');
      }

      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download failed:', error);
      alert('Failed to download history. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      className="btn btn-primary download-button"
      onClick={handleDownload}
      disabled={loading}
    >
      {loading ? (
        <>
          <span className="loading-spinner"></span>
          Downloading...
        </>
      ) : (
        'Download History as Excel'
      )}
    </button>
  );
};

export default DownloadButton;



