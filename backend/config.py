"""
Configuration management for Flask application.
Loads settings from environment variables with sensible defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.parent
BACKEND_DIR = Path(__file__).parent


class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Email configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', '172.24.128.80')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 25))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'False').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'cutting_fb@murata.com')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME', 'cutting_fb@murata.com')
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(BACKEND_DIR, 'uploads')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB default
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    
    # Excel file paths
    HISTORY_A1_PATH = os.path.join(BASE_DIR, 'history_A1.xlsx')
    HISTORY_GHM_PATH = os.path.join(BASE_DIR, 'history_GHM.xlsx')
    HISTORY_KEM_PATH = os.path.join(BASE_DIR, 'history_KEM.xlsx')
    
    # Image path
    IMAGE_PATH = os.path.join(BASE_DIR, 'cutfb.png')
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Email recipient lists (moved from hardcoded values)
    EMAIL_RECIPIENTS_A1 = [
        'perry.ong@murata.com',
        'mahesh.subramanian@murata.com',
        'jianfeng.yin@murata.com',
        'k.gopinath@murata.com',
        'keigo.inata@murata.com',
        'kumarsamy.mascow@murata.com',
        'kursi.hanifaansarulla@murata.com',
        'freddy.fong@murata.com',
        'lemuel.viernes@murata.com',
        'muklesur.rahman@murata.com',
        'norzairey.binzainal@murata.com',
        'ramesh.jayabalan@murata.com',
        'ramkumar.venk@murata.com',
        'reluvanullah.s@murata.com',
        'gg.sankar@murata.com',
        'yingping.foo@murata.com',
        'gurunathan.kum@murata.com',
        'sellamuthu.shamugam@murata.com',
        'woontak.tang@murata.com',
        'shooni.khor@murata.com',
        'chyansiang.goh@murata.com',
        'zhengpiau.tay@murata.com',
        'logenthan.ramachenderan@murata.com',
        'yogakumaran.krishnan@murata.com',
        'junhui.zou@murata.com',
        'kaidi.yau@murata.com',
        'menghui.choy@murata.com',
        'thiruppathi.balamurugan@murata.com',
        'xudong.pan@murata.com',
        'hywell.chong@murata.com'
    ]
    
    EMAIL_RECIPIENTS_GHM = EMAIL_RECIPIENTS_A1.copy()  # Same as A1
    
    EMAIL_RECIPIENTS_KEM = [
        'perry.ong@murata.com',
        'mahesh.subramanian@murata.com',
        'k.gopinath@murata.com',
        'kumarsamy.mascow@murata.com',
        'logenthan.ramachenderan@murata.com',
        'ramesh.jayabalan@murata.com',
        'yogakumaran.krishnan@murata.com',
        'reluvanullah.s@murata.com'
    ]


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

