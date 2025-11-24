"""
Excel service for thread-safe Excel file operations.
"""
from flask import current_app
import pandas as pd
import os
import threading
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Thread locks for each history file
_locks = {
    'a1': threading.Lock(),
    'ghm': threading.Lock(),
    'kem': threading.Lock()
}


class ExcelService:
    """Service for handling Excel file operations."""
    
    @staticmethod
    def get_history_path(form_type: str) -> str:
        """
        Get history file path for form type.
        
        Args:
            form_type: Type of form ('a1', 'ghm', 'kem')
        
        Returns:
            Path to history Excel file
        """
        path_map = {
            'a1': current_app.config['HISTORY_A1_PATH'],
            'ghm': current_app.config['HISTORY_GHM_PATH'],
            'kem': current_app.config['HISTORY_KEM_PATH']
        }
        return path_map.get(form_type.lower())
    
    @staticmethod
    def get_history_columns(form_type: str) -> List[str]:
        """
        Get column names for history DataFrame based on form type.
        
        Args:
            form_type: Type of form ('a1', 'ghm', 'kem')
        
        Returns:
            List of column names
        """
        if form_type.lower() == 'a1':
            return [
                'Date and Time', 'Lot Number', 'Item Type', 'GSX Machine No', 
                'MC Machine No', 'Cut Operator Payroll', 'NG Block/Lot',
                'NG chip Qty/Lot(pcs)', 'Block Number', 'Confirm Date', 'Reason', 
                'Defects', 'Judgement Block A', 'Judgement Block B', 
                'Judgement Block C', 'Judgement Block D', 'Shifting Amount A', 
                'Shifting Amount B', 'Shifting Amount C', 'Shifting Amount D', 
                'Shifting Direction A', 'Shifting Direction B', 
                'Shifting Direction C', 'Shifting Direction D', 'Quality Case',
                'Process select'
            ]
        elif form_type.lower() == 'ghm':
            return [
                'Date and Time', 'Lot Number', 'Item Type', 'MLN Machine No', 
                'MC Machine No', 'Cut Operator Payroll', 'NG Block/Lot', 
                'NG chip Qty/Lot(pcs)', 'Block Number', 'Confirm Date', 'Reason', 
                'Defects', 'Judgement', 'Shifting Amount', 'Shifting Direction', 
                'Quality_Case', 'Process select'
            ]
        elif form_type.lower() == 'kem':
            return [
                'Date and Time', 'Lot Number', 'Item Type', 'ERST Machine No', 
                'MC Machine No', 'Cut Operator Payroll', 'NG Block/Lot', 
                'NG chip Qty/Lot(pcs)', 'Block Number', 'Confirm Date', 'Reason', 
                'Defects', 'Judgement Block', 'Shifting Amount', 
                'Shifting Direction', 'Quality Case', 'Process select'
            ]
        else:
            raise ValueError(f"Unknown form type: {form_type}")
    
    @staticmethod
    def read_history(form_type: str) -> pd.DataFrame:
        """
        Read history from Excel file (thread-safe).
        
        Args:
            form_type: Type of form ('a1', 'ghm', 'kem')
        
        Returns:
            DataFrame with history data
        """
        history_path = ExcelService.get_history_path(form_type)
        lock = _locks[form_type.lower()]
        
        with lock:
            try:
                if os.path.exists(history_path):
                    df = pd.read_excel(history_path, engine='openpyxl')
                    logger.info(f"Read history from {history_path}: {len(df)} rows")
                    return df
                else:
                    # Create empty DataFrame with correct columns
                    columns = ExcelService.get_history_columns(form_type)
                    df = pd.DataFrame(columns=columns)
                    logger.info(f"Created new history file: {history_path}")
                    return df
            except Exception as e:
                logger.error(f"Failed to read history from {history_path}: {e}")
                raise
    
    @staticmethod
    def append_to_history(form_type: str, data: Dict) -> bool:
        """
        Append new entry to history Excel file (thread-safe).
        
        Args:
            form_type: Type of form ('a1', 'ghm', 'kem')
            data: Dictionary with form data to append
        
        Returns:
            True if successful, False otherwise
        """
        history_path = ExcelService.get_history_path(form_type)
        lock = _locks[form_type.lower()]
        
        with lock:
            try:
                # Read existing history
                if os.path.exists(history_path):
                    df = pd.read_excel(history_path, engine='openpyxl')
                else:
                    columns = ExcelService.get_history_columns(form_type)
                    df = pd.DataFrame(columns=columns)
                
                # Create new row
                new_row = pd.DataFrame([data])
                
                # Append and save
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_excel(history_path, index=False, engine='openpyxl')
                
                logger.info(f"Appended entry to {history_path}")
                return True
                
            except Exception as e:
                logger.error(f"Failed to append to history {history_path}: {e}")
                return False
    
    @staticmethod
    def get_history_as_dict(form_type: str) -> List[Dict]:
        """
        Get history as list of dictionaries.
        
        Args:
            form_type: Type of form ('a1', 'ghm', 'kem')
        
        Returns:
            List of dictionaries representing history rows
        """
        df = ExcelService.read_history(form_type)
        # Convert DataFrame to list of dicts, handling NaN values
        return df.fillna('').to_dict('records')
    
    @staticmethod
    def get_history_excel_bytes(form_type: str) -> bytes:
        """
        Get history Excel file as bytes for download.
        
        Args:
            form_type: Type of form ('a1', 'ghm', 'kem')
        
        Returns:
            Excel file as bytes
        """
        import io
        history_path = ExcelService.get_history_path(form_type)
        lock = _locks[form_type.lower()]
        
        with lock:
            try:
                if os.path.exists(history_path):
                    df = pd.read_excel(history_path, engine='openpyxl')
                else:
                    columns = ExcelService.get_history_columns(form_type)
                    df = pd.DataFrame(columns=columns)
                
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                return output.getvalue()
                
            except Exception as e:
                logger.error(f"Failed to generate Excel bytes for {form_type}: {e}")
                raise


