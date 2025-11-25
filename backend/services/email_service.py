"""
Email service for sending feedback emails with attachments.
"""
from flask import current_app
from flask_mail import Mail, Message
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for handling email operations."""
    
    def __init__(self, app=None):
        """
        Initialize email service.
        
        Args:
            app: Flask application instance
        """
        self.mail = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """
        Initialize Flask-Mail with app configuration.
        
        Args:
            app: Flask application instance
        """
        self.mail = Mail(app)
    
    def send_feedback_email(
        self,
        form_type: str,
        subject: str,
        body: str,
        photo_paths: List[str],
        grid_image_path: Optional[str] = None
    ) -> bool:
        """
        Send feedback email with attachments.
        
        Args:
            form_type: Type of form ('a1', 'ghm', 'kem')
            subject: Email subject
            body: Email body text
            photo_paths: List of photo file paths to attach
            grid_image_path: Optional grid image path to attach
        
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Get recipient list based on form type
            recipients = self._get_recipients(form_type)
            sender = current_app.config['MAIL_DEFAULT_SENDER']
            
            # Create message
            msg = Message(
                subject=subject,
                sender=sender,
                recipients=recipients,
                body=body
            )
            
            # Attach photos
            for photo_path in photo_paths:
                if photo_path:
                    try:
                        with open(photo_path, 'rb') as fp:
                            filename = photo_path.split('/')[-1]
                            msg.attach(filename, 'image/jpeg', fp.read())
                    except Exception as e:
                        logger.warning(f"Failed to attach photo {photo_path}: {e}")
            
            # Attach grid image if provided
            if grid_image_path:
                try:
                    with open(grid_image_path, 'rb') as fp:
                        filename = grid_image_path.split('/')[-1]
                        msg.attach(filename, 'image/png', fp.read())
                except Exception as e:
                    logger.warning(f"Failed to attach grid image {grid_image_path}: {e}")
            
            # Send email
            self.mail.send(msg)
            logger.info(f"Email sent successfully to {len(recipients)} recipients")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def _get_recipients(self, form_type: str) -> List[str]:
        """
        Get recipient list for form type.
        
        Args:
            form_type: Type of form ('a1', 'ghm', 'kem')
        
        Returns:
            List of email addresses
        """
        config_key = f'EMAIL_RECIPIENTS_{form_type.upper()}'
        return current_app.config.get(config_key, [])
    
    @staticmethod
    def format_email_body_a1(data: dict) -> str:
        """
        Format email body for A1 cutting feedback.
        
        Args:
            data: Form data dictionary
        
        Returns:
            Formatted email body string
        """
        return (
            f"Reason: {', '.join(data.get('reason', []))}\n"
            f"Date and Time: {data.get('date_time', '')}\n"
            f"Lot Number: {data.get('lot_number', '')}\n"
            f"Item Type: {data.get('item_type', '')}\n"
            f"GSX Machine No: {data.get('gsx_machine_no', '')}\n"
            f"MC Machine No: {data.get('mc_machine_no', '')}\n"
            f"Cut Operator Payroll: {data.get('cut_operator_payroll', '')}\n"
            f"NG Block/Lot: {data.get('ng_block_lot', '')}\n"
            f"NG chip Qty/Lot(pcs): {data.get('ng_chip_qty_lot', '')}\n"
            f"Block Number: {data.get('block_number', '')}\n"
            f"Confirm Date: {data.get('confirm_date', '')}\n"
            f"Defects: {', '.join(data.get('defects', []))}\n"
            f"Judgement Block A: {data.get('judgement_block_a', '')}\n"
            f"Judgement Block B: {data.get('judgement_block_b', '')}\n"
            f"Judgement Block C: {data.get('judgement_block_c', '')}\n"
            f"Judgement Block D: {data.get('judgement_block_d', '')}\n"
            f"Shifting Amount A: {data.get('shifting_amount_a', '')}\n"
            f"Shifting Amount B: {data.get('shifting_amount_b', '')}\n"
            f"Shifting Amount C: {data.get('shifting_amount_c', '')}\n"
            f"Shifting Amount D: {data.get('shifting_amount_d', '')}\n"
            f"Shifting Direction A: {', '.join(data.get('shifting_direction_a', []))}\n"
            f"Shifting Direction B: {', '.join(data.get('shifting_direction_b', []))}\n"
            f"Shifting Direction C: {', '.join(data.get('shifting_direction_c', []))}\n"
            f"Shifting Direction D: {', '.join(data.get('shifting_direction_d', []))}\n"
            f"Quality Case: {data.get('quality_case', '')}\n"
            f"Process select: {', '.join(data.get('process_selection', []))}\n"
        )
    
    @staticmethod
    def format_email_body_ghm(data: dict) -> str:
        """
        Format email body for GHM cutting feedback.
        
        Args:
            data: Form data dictionary
        
        Returns:
            Formatted email body string
        """
        return (
            f"Date and Time: {data.get('date_time', '')}\n"
            f"Lot Number: {data.get('lot_number', '')}\n"
            f"Item Type: {data.get('item_type', '')}\n"
            f"MLN Machine No: {data.get('mln_machine_no', '')}\n"
            f"MC Machine No: {data.get('mc_machine_no', '')}\n"
            f"Cut Operator Payroll: {data.get('cut_operator_payroll', '')}\n"
            f"NG Block/Lot: {data.get('ng_block_lot', '')}\n"
            f"NG chip Qty/Lot(pcs): {data.get('ng_chip_qty_lot', '')}\n"
            f"Block Number: {data.get('block_number', '')}\n"
            f"Confirm Date: {data.get('confirm_date', '')}\n"
            f"Reason: {', '.join(data.get('reason', []))}\n"
            f"Defects: {', '.join(data.get('defects', []))}\n"
            f"Judgement Block: {data.get('judgement', '')}\n"
            f"Shifting Amount: {data.get('shifting_amount', '')}\n"
            f"Shifting Direction: {', '.join(data.get('shifting_direction', []))}\n"
            f"Quality Case: {data.get('quality_case', '')}\n"
            f"Process select: {', '.join(data.get('process_selection', []))}\n"
        )
    
    @staticmethod
    def format_email_body_kem(data: dict) -> str:
        """
        Format email body for KEM cutting feedback.
        
        Args:
            data: Form data dictionary
        
        Returns:
            Formatted email body string
        """
        return (
            f"Date and Time: {data.get('date_time', '')}\n"
            f"Lot Number: {data.get('lot_number', '')}\n"
            f"Item Type: {data.get('item_type', '')}\n"
            f"ERST Machine No: {data.get('erst_machine_no', '')}\n"
            f"MC Machine No: {data.get('mc_machine_no', '')}\n"
            f"Cut Operator Payroll: {data.get('cut_operator_payroll', '')}\n"
            f"NG Block/Lot: {data.get('ng_block_lot', '')}\n"
            f"NG chip Qty/Lot(pcs): {data.get('ng_chip_qty_lot', '')}\n"
            f"Block Number: {data.get('block_number', '')}\n"
            f"Confirm Date: {data.get('confirm_date', '')}\n"
            f"Reason: {', '.join(data.get('reason', []))}\n"
            f"Defects: {', '.join(data.get('defects', []))}\n"
            f"Judgement Block: {data.get('judgement', '')}\n"
            f"Shifting Amount: {data.get('shifting_amount', '')}\n"
            f"Shifting Direction: {', '.join(data.get('shifting_direction', []))}\n"
            f"Quality Case: {data.get('quality_case', '')}\n"
            f"Process select: {', '.join(data.get('process_selection', []))}\n"
        )



