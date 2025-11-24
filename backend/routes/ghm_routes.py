"""
API routes for GHM cutting process feedback.
"""
from flask import Blueprint, request, jsonify, send_file
from flask import current_app
from models.schemas import GHMFormSchema
from services.email_service import EmailService
from services.file_service import FileService
from services.excel_service import ExcelService
from services.grid_service import GridService
import io
import json
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('ghm', __name__)
schema = GHMFormSchema()


def get_email_service():
    """Get email service instance."""
    from services.email_service import EmailService
    return EmailService()


@bp.route('/submit', methods=['POST'])
def submit():
    """
    Submit GHM cutting process feedback form.
    """
    try:
        # Get form data
        if 'data' in request.form:
            form_data = json.loads(request.form['data'])
        else:
            form_data = {
                'date_time': request.form.get('date_time'),
                'lot_number': request.form.get('lot_number'),
                'item_type': request.form.get('item_type'),
                'mln_machine_no': request.form.get('mln_machine_no'),
                'mc_machine_no': request.form.get('mc_machine_no'),
                'cut_operator_payroll': request.form.get('cut_operator_payroll'),
                'ng_block_lot': request.form.get('ng_block_lot'),
                'ng_chip_qty_lot': request.form.get('ng_chip_qty_lot'),
                'block_number': request.form.get('block_number'),
                'confirm_date': request.form.get('confirm_date'),
                'reason': request.form.getlist('reason') if 'reason' in request.form else json.loads(request.form.get('reason', '[]')),
                'defects': request.form.getlist('defects') if 'defects' in request.form else json.loads(request.form.get('defects', '[]')),
                'judgement': request.form.get('judgement'),
                'shifting_amount': request.form.get('shifting_amount'),
                'shifting_direction': request.form.getlist('shifting_direction') if 'shifting_direction' in request.form else json.loads(request.form.get('shifting_direction', '[]')),
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
        
        # Generate date-time string
        date_time_str = form_data['date_time'].replace(" ", "_").replace(":", "-")
        
        # Save files
        upload_dir = current_app.config['UPLOAD_FOLDER']
        photo_paths = FileService.save_files(valid_files, 'ghm', date_time_str)
        
        # Generate grid image
        grid_data = form_data['grid']
        grid_image_path = GridService.generate_grid_image(
            'ghm',
            grid_data,
            f"{upload_dir}/ghm",
            date_time_str
        )
        
        # Format email body
        email_body = EmailService.format_email_body_ghm(form_data)
        
        # Send email
        email_service = get_email_service()
        email_service.init_app(current_app)
        email_sent = email_service.send_feedback_email(
            'ghm',
            'Details Submitted - GHM Cutting Feedback',
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
            'MLN Machine No': form_data['mln_machine_no'],
            'MC Machine No': form_data['mc_machine_no'],
            'Cut Operator Payroll': form_data['cut_operator_payroll'],
            'NG Block/Lot': form_data['ng_block_lot'],
            'NG chip Qty/Lot(pcs)': form_data['ng_chip_qty_lot'],
            'Block Number': form_data['block_number'],
            'Confirm Date': form_data['confirm_date'],
            'Reason': ', '.join(form_data['reason']),
            'Defects': ', '.join(form_data['defects']),
            'Judgement': form_data['judgement'],
            'Shifting Amount': form_data['shifting_amount'],
            'Shifting Direction': ', '.join(form_data['shifting_direction']),
            'Quality_Case': form_data['quality_case'],
            'Process select': ', '.join(form_data['process_selection'])
        }
        
        # Save to Excel
        success = ExcelService.append_to_history('ghm', excel_data)
        if not success:
            return jsonify({'error': 'Failed to save to history'}), 500
        
        return jsonify({
            'message': 'Form submitted successfully',
            'email_sent': email_sent
        }), 200
        
    except Exception as e:
        logger.error(f"Error in GHM submit: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


@bp.route('/history', methods=['GET'])
def get_history():
    """Get GHM cutting process feedback history."""
    try:
        history = ExcelService.get_history_as_dict('ghm')
        return jsonify(history), 200
    except Exception as e:
        logger.error(f"Error getting GHM history: {e}", exc_info=True)
        return jsonify({'error': 'Failed to retrieve history', 'message': str(e)}), 500


@bp.route('/history/download', methods=['GET'])
def download_history():
    """Download GHM cutting process feedback history as Excel file."""
    try:
        excel_bytes = ExcelService.get_history_excel_bytes('ghm')
        return send_file(
            io.BytesIO(excel_bytes),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='history_GHM.xlsx'
        )
    except Exception as e:
        logger.error(f"Error downloading GHM history: {e}", exc_info=True)
        return jsonify({'error': 'Failed to download history', 'message': str(e)}), 500

