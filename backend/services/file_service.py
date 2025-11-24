"""
File service for handling file uploads and validation.
"""
from flask import current_app
from werkzeug.utils import secure_filename
from typing import List, Tuple
import os
import logging

logger = logging.getLogger(__name__)


class FileService:
    """Service for handling file operations."""
    
    @staticmethod
    def allowed_file(filename: str) -> bool:
        """
        Check if file extension is allowed.
        
        Args:
            filename: Name of the file
        
        Returns:
            True if file extension is allowed, False otherwise
        """
        if '.' not in filename:
            return False
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in current_app.config['ALLOWED_EXTENSIONS']
    
    @staticmethod
    def validate_files(files: List) -> Tuple[bool, str, List]:
        """
        Validate uploaded files.
        
        Args:
            files: List of file objects from request
        
        Returns:
            Tuple of (is_valid, error_message, valid_files)
        """
        if not files:
            return False, "No files provided", []
        
        valid_files = []
        max_size = current_app.config['MAX_FILE_SIZE']
        
        for file in files:
            # Check filename
            if not file.filename:
                continue
            
            # Check extension
            if not FileService.allowed_file(file.filename):
                return False, f"File {file.filename} has invalid extension. Allowed: jpg, jpeg, png", []
            
            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)  # Reset file pointer
            
            if file_size > max_size:
                return False, f"File {file.filename} exceeds maximum size of {max_size} bytes", []
            
            valid_files.append(file)
        
        if not valid_files:
            return False, "No valid files provided", []
        
        return True, "", valid_files
    
    @staticmethod
    def save_files(files: List, form_type: str, date_time_str: str) -> List[str]:
        """
        Save uploaded files to disk.
        
        Args:
            files: List of validated file objects
            form_type: Type of form ('a1', 'ghm', 'kem')
            date_time_str: Date-time string for unique naming
        
        Returns:
            List of saved file paths
        """
        upload_dir = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            form_type
        )
        os.makedirs(upload_dir, exist_ok=True)
        
        saved_paths = []
        
        for idx, file in enumerate(files):
            # Secure filename and add timestamp for uniqueness
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            unique_filename = f"{name}_{date_time_str}_{idx}{ext}"
            
            file_path = os.path.join(upload_dir, unique_filename)
            
            try:
                file.save(file_path)
                saved_paths.append(file_path)
                logger.info(f"File saved: {file_path}")
            except Exception as e:
                logger.error(f"Failed to save file {filename}: {e}")
                raise
        
        return saved_paths
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        Delete a file from disk.
        
        Args:
            file_path: Path to file to delete
        
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
            return False


