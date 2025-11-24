"""
Grid service for generating grid images from selection data.
"""
from flask import current_app
from PIL import Image, ImageDraw
from typing import List, Optional
import os
import logging

logger = logging.getLogger(__name__)


class GridService:
    """Service for generating grid images."""
    
    @staticmethod
    def generate_grid_image_a1(
        grid_data: List[List[bool]],
        output_path: str,
        date_time_str: str
    ) -> str:
        """
        Generate 6x6 grid image for A1 with colored blocks.
        
        A1 grid layout:
        - Rows 0-2: Blocks A (left 3) and B (right 3)
        - Rows 3-5: Blocks C (left 3) and D (right 3)
        
        Colors:
        - A: Red
        - B: Green
        - C: Blue
        - D: Yellow
        
        Args:
            grid_data: 6x6 2D list of booleans (selected cells)
            output_path: Directory to save the image
            date_time_str: Date-time string for unique filename
        
        Returns:
            Path to generated image file
        """
        # Create image (360x360 pixels, 60px per cell)
        image = Image.new('RGB', (360, 360), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # Block colors
        block_colors = {
            'A': (255, 0, 0),      # Red
            'B': (0, 255, 0),      # Green
            'C': (0, 0, 255),      # Blue
            'D': (255, 240, 0)     # Yellow
        }
        
        # Draw grid cells
        for i in range(6):
            for j in range(6):
                # Determine block
                if i < 3:
                    block = 'A' if j < 3 else 'B'
                else:
                    block = 'C' if j < 3 else 'D'
                
                # Cell coordinates
                x1 = j * 60
                y1 = i * 60
                x2 = x1 + 60
                y2 = y1 + 60
                
                # Fill color based on selection and block
                if grid_data[i][j]:
                    # Selected: use block color with transparency
                    fill_color = block_colors[block]
                else:
                    # Not selected: white
                    fill_color = (255, 255, 255)
                
                # Draw rectangle
                draw.rectangle([x1, y1, x2, y2], outline='black', fill=fill_color)
                
                # Add block label
                if grid_data[i][j]:
                    # Center text in cell
                    text_x = x1 + 30
                    text_y = y1 + 30
                    draw.text((text_x - 5, text_y - 5), block, fill='black')
        
        # Save image
        os.makedirs(output_path, exist_ok=True)
        filename = f'grid_image_{date_time_str}.png'
        file_path = os.path.join(output_path, filename)
        image.save(file_path)
        
        logger.info(f"Generated A1 grid image: {file_path}")
        return file_path
    
    @staticmethod
    def generate_grid_image_ghm_kem(
        grid_data: List[List[bool]],
        output_path: str,
        date_time_str: str
    ) -> str:
        """
        Generate 3x3 grid image for GHM/KEM.
        
        Args:
            grid_data: 3x3 2D list of booleans (selected cells)
            output_path: Directory to save the image
            date_time_str: Date-time string for unique filename
        
        Returns:
            Path to generated image file
        """
        # Create image (180x180 pixels, 60px per cell)
        image = Image.new('RGB', (180, 180), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # Draw grid cells
        for i in range(3):
            for j in range(3):
                # Cell coordinates
                x1 = j * 60
                y1 = i * 60
                x2 = x1 + 60
                y2 = y1 + 60
                
                # Fill color based on selection
                if grid_data[i][j]:
                    fill_color = (255, 0, 0)  # Red for selected
                else:
                    fill_color = (255, 255, 255)  # White for not selected
                
                # Draw rectangle
                draw.rectangle([x1, y1, x2, y2], outline='black', fill=fill_color)
        
        # Save image
        os.makedirs(output_path, exist_ok=True)
        filename = f'grid_image_{date_time_str}.png'
        file_path = os.path.join(output_path, filename)
        image.save(file_path)
        
        logger.info(f"Generated grid image: {file_path}")
        return file_path
    
    @staticmethod
    def generate_grid_image(
        form_type: str,
        grid_data: List[List[bool]],
        output_path: str,
        date_time_str: str
    ) -> str:
        """
        Generate grid image based on form type.
        
        Args:
            form_type: Type of form ('a1', 'ghm', 'kem')
            grid_data: 2D list of booleans representing grid selection
            output_path: Directory to save the image
            date_time_str: Date-time string for unique filename
        
        Returns:
            Path to generated image file
        """
        if form_type.lower() == 'a1':
            return GridService.generate_grid_image_a1(grid_data, output_path, date_time_str)
        elif form_type.lower() in ['ghm', 'kem']:
            return GridService.generate_grid_image_ghm_kem(grid_data, output_path, date_time_str)
        else:
            raise ValueError(f"Unknown form type: {form_type}")

