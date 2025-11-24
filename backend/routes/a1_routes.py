"""
API routes for A1 cutting process feedback.
"""
from flask import Blueprint, request, jsonify, send_file
from flask import current_app
from models.schemas import A1FormSchema
from services.email_service import EmailService
from services.file_service import FileService
from services.excel_service import ExcelService
from services.grid_service import GridService
from datetime import datetime
import io
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('a1', __name__)
schema = A1FormSchema()


def get_email_service():
    """Get email service instance."""
    from services.email_service import EmailService
    return EmailService()


@bp.route('/submit', methods=['POST'])
def submit():
    """
    Submit A1 cutting process feedback form.
    
    Expected request:
    - multipart/form-data with form fields and files
    - Files: 'photos' (multiple files)
    - Form data: JSON string in 'data' field or individual fields
    """
    try:
        # Get form data
        if 'data' in request.form:
            # JSON data in form field
            import json
            form_data = json.loads(request.form['data'])
        else:
            # Individual form fields
            form_data = {
                'date_time': request.form.get('date_time'),
                'lot_number': request.form.get('lot_number'),
                'item_type': request.form.get('item_type'),
                'gsx_machine_no': request.form.get('gsx_machine_no'),
                'mc_machine_no': request.form.get('mc_machine_no'),
                'cut_operator_payroll': request.form.get('cut_operator_payroll'),
                'ng_block_lot': request.form.get('ng_block_lot'),
                'ng_chip_qty_lot': request.form.get('ng_chip_qty_lot'),
                'block_number': request.form.get('block_number'),
                'confirm_date': request.form.get('confirm_date'),
                'reason': request.form.getlist('reason') if 'reason' in request.form else json.loads(request.form.get('reason', '[]')),
                'defects': request.form.getlist('defects') if 'defects' in request.form else json.loads(request.form.get('defects', '[]')),
                'judgement_block_a': request.form.get('judgement_block_a'),
                'judgement_block_b': request.form.get('judgement_block_b'),
                'judgement_block_c': request.form.get('judgement_block_c'),
                'judgement_block_d': request.form.get('judgement_block_d'),
                'shifting_amount_a': request.form.get('shifting_amount_a'),
                'shifting_amount_b': request.form.get('shifting_amount_b'),
                'shifting_amount_c': request.form.get('shifting_amount_c'),
                'shifting_amount_d': request.form.get('shifting_amount_d'),
                'shifting_direction_a': request.form.getlist('shifting_direction_a') if 'shifting_direction_a' in request.form else json.loads(request.form.get('shifting_direction_a', '[]')),
                'shifting_direction_b': request.form.getlist('shifting_direction_b') if 'shifting_direction_b' in request.form else json.loads(request.form.get('shifting_direction_b', '[]')),
                'shifting_direction_c': request.form.getlist('shifting_direction_c') if 'shifting_direction_c' in request.form else json.loads(request.form.get('shifting_direction_c', '[]')),
                'shifting_direction_d': request.form.getlist('shifting_direction_d') if 'shifting_direction_d' in request.form else json.loads(request.form.get('shifting_direction_d', '[]')),
                'quality_case': request.form.get('quality_case'),
                'process_selection': request.form.getlist('process_selection') if 'process_selection' in request.form else json.loads(request.form.get('process_selection', '[]')),
                'grid': json.loads(request.form.get('grid', '[]'))
            }
        
        # Validate form data
        errors = schema.validate(form_data)
        if errors:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400
        
        # Get and validate files
        files = request.files.getlist('photos')
        is_valid, error_msg, valid_files = FileService.validate_files(files)
        if not is_valid:
            return jsonify({'error': 'File validation failed', 'message': error_msg}), 400
        
        # Generate date-time string for file naming
        date_time_str = form_data['date_time'].replace(" ", "_").replace(":", "-")
        
        # Save files
        upload_dir = current_app.config['UPLOAD_FOLDER']
        photo_paths = FileService.save_files(valid_files, 'a1', date_time_str)
        
        # Generate grid image
        grid_data = form_data['grid']
        grid_image_path = GridService.generate_grid_image(
            'a1',
            grid_data,
            f"{upload_dir}/a1",
            date_time_str
        )
        
        # Format email body
        email_body = EmailService.format_email_body_a1(form_data)
        
        # Send email
        email_service = get_email_service()
        email_service.init_app(current_app)
        email_sent = email_service.send_feedback_email(
            'a1',
            'Details Submitted - A1 Cutting Feedback',
            email_body,
            photo_paths,
            grid_image_path
        )
        
        if not email_sent:
            logger.warning("Email sending failed, but continuing with data save")
        
        # Prepare data for Excel
        excel_data = {
            'Date and Time': form_data['date_time'],
            'Lot Number': form_data['lot_number'],
            'Item Type': form_data['item_type'],
            'GSX Machine No': form_data['gsx_machine_no'],
            'MC Machine No': form_data['mc_machine_no'],
            'Cut Operator Payroll': form_data['cut_operator_payroll'],
            'NG Block/Lot': form_data['ng_block_lot'],
            'NG chip Qty/Lot(pcs)': form_data['ng_chip_qty_lot'],
            'Block Number': form_data['block_number'],
            'Confirm Date': form_data['confirm_date'],
            'Reason': ', '.join(form_data['reason']),
            'Defects': ', '.join(form_data['defects']),
            'Judgement Block A': form_data['judgement_block_a'],
            'Judgement Block B': form_data['judgement_block_b'],
            'Judgement Block C': form_data['judgement_block_c'],
            'Judgement Block D': form_data['judgement_block_d'],
            'Shifting Amount A': form_data['shifting_amount_a'],
            'Shifting Amount B': form_data['shifting_amount_b'],
            'Shifting Amount C': form_data['shifting_amount_c'],
            'Shifting Amount D': form_data['shifting_amount_d'],
            'Shifting Direction A': ', '.join(form_data['shifting_direction_a']),
            'Shifting Direction B': ', '.join(form_data['shifting_direction_b']),
            'Shifting Direction C': ', '.join(form_data['shifting_direction_c']),
            'Shifting Direction D': ', '.join(form_data['shifting_direction_d']),
            'Quality Case': form_data['quality_case'],
            'Process select': ', '.join(form_data['process_selection'])
        }
        
        # Save to Excel
        success = ExcelService.append_to_history('a1', excel_data)
        if not success:
            return jsonify({'error': 'Failed to save to history'}), 500
        
        return jsonify({
            'message': 'Form submitted successfully',
            'email_sent': email_sent
        }), 200
        
    except Exception as e:
        logger.error(f"Error in A1 submit: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


@bp.route('/history', methods=['GET'])
def get_history():
    """
    Get A1 cutting process feedback history.
    
    Returns:
        JSON array of history records
    """
    try:
        history = ExcelService.get_history_as_dict('a1')
        return jsonify(history), 200
    except Exception as e:
        logger.error(f"Error getting A1 history: {e}", exc_info=True)
        return jsonify({'error': 'Failed to retrieve history', 'message': str(e)}), 500


@bp.route('/history/download', methods=['GET'])
def download_history():
    """
    Download A1 cutting process feedback history as Excel file.
    
    Returns:
        Excel file download
    """
    try:
        excel_bytes = ExcelService.get_history_excel_bytes('a1')
        return send_file(
            io.BytesIO(excel_bytes),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='history_A1.xlsx'
        )
    except Exception as e:
        logger.error(f"Error downloading A1 history: {e}", exc_info=True)
        return jsonify({'error': 'Failed to download history', 'message': str(e)}), 500

