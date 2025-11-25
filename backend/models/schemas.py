"""
Marshmallow schemas for form validation.
"""
from marshmallow import Schema, fields, validate, ValidationError, validates_schema
from typing import List


class GridDataSchema(Schema):
    """Schema for grid selection data."""
    grid = fields.List(
        fields.List(fields.Bool()),
        required=True,
        validate=validate.Length(min=1)
    )
    
    @validates_schema
    def validate_grid_size(self, data, **kwargs):
        """Validate grid size based on form type."""
        grid = data.get('grid', [])
        if not grid:
            raise ValidationError("Grid data is required")
        
        # Check if it's a 2D list
        if not all(isinstance(row, list) for row in grid):
            raise ValidationError("Grid must be a 2D array")
        
        # Validate row lengths are consistent
        if grid:
            row_length = len(grid[0])
            if not all(len(row) == row_length for row in grid):
                raise ValidationError("All grid rows must have the same length")


class A1FormSchema(Schema):
    """Schema for A1 cutting process feedback form."""
    
    # Basic information
    date_time = fields.Str(required=True, validate=validate.Length(min=1))
    lot_number = fields.Str(required=True, validate=validate.Length(min=1, max=10))
    item_type = fields.Str(required=True, validate=validate.Length(min=1))
    gsx_machine_no = fields.Str(required=True, validate=validate.Length(min=1))
    mc_machine_no = fields.Str(required=True, validate=validate.Length(min=1))
    cut_operator_payroll = fields.Str(required=True, validate=validate.Length(min=1))
    ng_block_lot = fields.Str(required=True, validate=validate.Length(min=1))
    ng_chip_qty_lot = fields.Str(required=True, validate=validate.Length(min=1))
    block_number = fields.Str(required=True, validate=validate.Length(min=1))
    confirm_date = fields.Str(required=True, validate=validate.Length(min=1))
    
    # Reason and defects
    reason = fields.List(
        fields.Str(validate=validate.OneOf(['After Repair', 'After Shut Down', 'Change item', 'Others'])),
        required=True,
        validate=validate.Length(min=1)
    )
    defects = fields.List(
        fields.Str(validate=validate.OneOf([
            'w shift', 'L shift', 'Sheet NG', 'W out/ Lout', 'Deformed', 
            'Slant Cut', 'Pattern dent', 'Dragging', 'Smearing', 'Partial print', 
            'Blunt cut', 'Others', 'Rough cut', 'VP dent', 'Line', 'Step Shift', 
            'Ridge/Dent', 'Cut Debris', 'Drop Chip', 'Electrode Horn', 'Blade Broken'
        ])),
        required=True,
        validate=validate.Length(min=1)
    )
    
    # Judgement blocks
    judgement_block_a = fields.Str(required=True, validate=validate.OneOf(['Good', 'NG']))
    judgement_block_b = fields.Str(required=True, validate=validate.OneOf(['Good', 'NG']))
    judgement_block_c = fields.Str(required=True, validate=validate.OneOf(['Good', 'NG']))
    judgement_block_d = fields.Str(required=True, validate=validate.OneOf(['Good', 'NG']))
    
    # Shifting amounts
    shifting_amount_a = fields.Str(required=True, validate=validate.Length(min=1))
    shifting_amount_b = fields.Str(required=True, validate=validate.Length(min=1))
    shifting_amount_c = fields.Str(required=True, validate=validate.Length(min=1))
    shifting_amount_d = fields.Str(required=True, validate=validate.Length(min=1))
    
    # Shifting directions
    shifting_direction_a = fields.List(
        fields.Str(validate=validate.OneOf(['W shift front', 'W shift back', 'L shift right', 'L shift left', 'Sheet NG', 'good'])),
        required=True,
        validate=validate.Length(min=1)
    )
    shifting_direction_b = fields.List(
        fields.Str(validate=validate.OneOf(['W shift front', 'W shift back', 'L shift right', 'L shift left', 'Sheet NG', 'good'])),
        required=True,
        validate=validate.Length(min=1)
    )
    shifting_direction_c = fields.List(
        fields.Str(validate=validate.OneOf(['W shift front', 'W shift back', 'L shift right', 'L shift left', 'Sheet NG', 'good'])),
        required=True,
        validate=validate.Length(min=1)
    )
    shifting_direction_d = fields.List(
        fields.Str(validate=validate.OneOf(['W shift front', 'W shift back', 'L shift right', 'L shift left', 'Sheet NG', 'good'])),
        required=True,
        validate=validate.Length(min=1)
    )
    
    # Quality case and process
    quality_case = fields.Str(required=True, validate=validate.OneOf(['open', 'close']))
    process_selection = fields.List(
        fields.Str(validate=validate.OneOf(['Stacking Feedback', 'Cutting Feedback'])),
        required=True,
        validate=validate.Length(min=1)
    )
    
    # Grid data (6x6 for A1)
    grid = fields.List(
        fields.List(fields.Bool()),
        required=True,
        validate=validate.Length(equal=6)
    )
    
    @validates_schema
    def validate_grid_size(self, data, **kwargs):
        """Validate A1 grid is 6x6."""
        grid = data.get('grid', [])
        if len(grid) != 6:
            raise ValidationError("Grid must have 6 rows")
        if not all(len(row) == 6 for row in grid):
            raise ValidationError("Each grid row must have 6 columns")


class GHMFormSchema(Schema):
    """Schema for GHM cutting process feedback form."""
    
    # Basic information
    date_time = fields.Str(required=True, validate=validate.Length(min=1))
    lot_number = fields.Str(required=True, validate=validate.Length(min=1))
    item_type = fields.Str(required=True, validate=validate.Length(min=1))
    mln_machine_no = fields.Str(required=True, validate=validate.Length(min=1))
    mc_machine_no = fields.Str(required=True, validate=validate.Length(min=1))
    cut_operator_payroll = fields.Str(required=True, validate=validate.Length(min=1))
    ng_block_lot = fields.Str(required=True, validate=validate.Length(min=1))
    ng_chip_qty_lot = fields.Str(required=True, validate=validate.Length(min=1))
    block_number = fields.Str(required=True, validate=validate.Length(min=1))
    confirm_date = fields.Str(required=True, validate=validate.Length(min=1))
    
    # Reason and defects
    reason = fields.List(
        fields.Str(validate=validate.OneOf(['After Repair', 'After Shut Down', 'Change item', 'Others'])),
        required=True,
        validate=validate.Length(min=1)
    )
    defects = fields.List(
        fields.Str(validate=validate.OneOf([
            'w shift', 'L shift', 'Sheet NG', 'W out/ Lout', 'Deformed', 
            'Slant Cut', 'Pattern dent', 'Smearing', 'Partial print', 
            'Blunt cut', 'Others', 'Rough cut', 'VP dent', 'Step Shift', 
            'Ridge/Dent', 'Sample', 'Drop Chips'
        ])),
        required=True,
        validate=validate.Length(min=1)
    )
    
    # Judgement
    judgement = fields.Str(required=True, validate=validate.OneOf(['Good', 'NG']))
    
    # Shifting
    shifting_amount = fields.Str(required=True, validate=validate.Length(min=1))
    shifting_direction = fields.List(
        fields.Str(validate=validate.OneOf(['W shift front', 'W shift back', 'L shift right', 'L shift left', 'Sheet NG', 'good'])),
        required=True,
        validate=validate.Length(min=1)
    )
    
    # Quality case and process
    quality_case = fields.Str(required=True, validate=validate.OneOf(['open', 'close']))
    process_selection = fields.List(
        fields.Str(validate=validate.OneOf(['Stacking Feedback', 'Cutting Feedback'])),
        required=True,
        validate=validate.Length(min=1)
    )
    
    # Grid data (3x3 for GHM)
    grid = fields.List(
        fields.List(fields.Bool()),
        required=True,
        validate=validate.Length(equal=3)
    )
    
    @validates_schema
    def validate_grid_size(self, data, **kwargs):
        """Validate GHM grid is 3x3."""
        grid = data.get('grid', [])
        if len(grid) != 3:
            raise ValidationError("Grid must have 3 rows")
        if not all(len(row) == 3 for row in grid):
            raise ValidationError("Each grid row must have 3 columns")


class KEMFormSchema(Schema):
    """Schema for KEM cutting process feedback form."""
    
    # Basic information
    date_time = fields.Str(required=True, validate=validate.Length(min=1))
    lot_number = fields.Str(required=True, validate=validate.Length(min=1, max=10))
    item_type = fields.Str(required=True, validate=validate.Length(min=1))
    erst_machine_no = fields.Str(required=True, validate=validate.Length(min=1))
    mc_machine_no = fields.Str(required=True, validate=validate.Length(min=1))
    cut_operator_payroll = fields.Str(required=True, validate=validate.Length(min=1))
    ng_block_lot = fields.Str(required=True, validate=validate.Length(min=1))
    ng_chip_qty_lot = fields.Str(required=True, validate=validate.Length(min=1))
    block_number = fields.Str(required=True, validate=validate.Length(min=1))
    confirm_date = fields.Str(required=True, validate=validate.Length(min=1))
    
    # Reason and defects
    reason = fields.List(
        fields.Str(validate=validate.OneOf(['After Repair', 'After Shut Down', 'Change item', 'Others'])),
        required=True,
        validate=validate.Length(min=1)
    )
    defects = fields.List(
        fields.Str(validate=validate.OneOf([
            'w shift', 'L shift', 'Sheet NG', 'W out/ Lout', 'Deformed', 
            'Slant Cut', 'Pattern dent', 'Smearing', 'Partial print', 
            'Blunt cut', 'Others', 'Rough cut', 'VP dent', 'Step Shift', 
            'Ridge/Dent'
        ])),
        required=True,
        validate=validate.Length(min=1)
    )
    
    # Judgement
    judgement = fields.Str(required=True, validate=validate.OneOf(['Good', 'NG']))
    
    # Shifting
    shifting_amount = fields.Str(required=True, validate=validate.Length(min=1))
    shifting_direction = fields.List(
        fields.Str(validate=validate.OneOf(['W shift front', 'W shift back', 'L shift right', 'L shift left', 'Sheet NG', 'good'])),
        required=True,
        validate=validate.Length(min=1)
    )
    
    # Quality case and process
    quality_case = fields.Str(required=True, validate=validate.OneOf(['open', 'close']))
    process_selection = fields.List(
        fields.Str(validate=validate.OneOf(['Stacking Feedback', 'Cutting Feedback'])),
        required=True,
        validate=validate.Length(min=1)
    )
    
    # Grid data (3x3 for KEM)
    grid = fields.List(
        fields.List(fields.Bool()),
        required=True,
        validate=validate.Length(equal=3)
    )
    
    @validates_schema
    def validate_grid_size(self, data, **kwargs):
        """Validate KEM grid is 3x3."""
        grid = data.get('grid', [])
        if len(grid) != 3:
            raise ValidationError("Grid must have 3 rows")
        if not all(len(row) == 3 for row in grid):
            raise ValidationError("Each grid row must have 3 columns")



