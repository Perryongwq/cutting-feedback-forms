"""
Flask application factory.
Creates and configures the Flask app instance.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from config import config
import os
import logging
from logging.handlers import RotatingFileHandler


def create_app(config_name=None):
    """
    Application factory pattern for Flask.
    
    Args:
        config_name: Configuration name ('development', 'production', 'testing')
                    Defaults to 'development' or FLASK_ENV env variable.
    
    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)
    
    # Determine configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app.config.from_object(config[config_name])
    
    # Initialize CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Setup logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/cutting_feedback.log',
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Cutting Feedback Application startup')
    
    # Create upload directories
    upload_dirs = [
        os.path.join(app.config['UPLOAD_FOLDER'], 'a1'),
        os.path.join(app.config['UPLOAD_FOLDER'], 'ghm'),
        os.path.join(app.config['UPLOAD_FOLDER'], 'kem')
    ]
    for upload_dir in upload_dirs:
        os.makedirs(upload_dir, exist_ok=True)
    
    # Initialize services
    from services.email_service import EmailService
    email_service = EmailService()
    email_service.init_app(app)
    
    # Register blueprints
    from routes import a1_routes, ghm_routes, kem_routes
    
    app.register_blueprint(a1_routes.bp, url_prefix='/api/a1')
    app.register_blueprint(ghm_routes.bp, url_prefix='/api/ghm')
    app.register_blueprint(kem_routes.bp, url_prefix='/api/kem')
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return jsonify({'error': 'Internal server error', 'message': 'An error occurred'}), 500
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'API is running'}), 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

