# Cutting Process Feedback - Backend API

Flask REST API backend for the Cutting Process Feedback application.

## Features

- RESTful API endpoints for A1, GHM, and KEM cutting process feedback
- Form validation using Marshmallow schemas
- File upload handling with validation
- Email sending with attachments
- Excel file operations (read/write) with thread safety
- Grid image generation
- History retrieval and download

## Project Structure

```
backend/
├── app.py                 # Flask application factory
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── routes/               # API route handlers
│   ├── a1_routes.py
│   ├── ghm_routes.py
│   └── kem_routes.py
├── services/             # Business logic services
│   ├── email_service.py
│   ├── file_service.py
│   ├── excel_service.py
│   └── grid_service.py
├── models/               # Data models and schemas
│   └── schemas.py
└── utils/                # Utility functions
    └── validators.py
```

## Installation

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Create necessary directories:**
   ```bash
   mkdir -p uploads/a1 uploads/ghm uploads/kem
   mkdir -p logs
   ```

## Configuration

Edit `.env` file with your settings:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Email Configuration
MAIL_SERVER=172.24.128.80
MAIL_PORT=25
MAIL_USE_TLS=False
MAIL_USE_SSL=False
MAIL_USERNAME=cutting_fb@murata.com

# File Upload
MAX_FILE_SIZE=10485760  # 10MB

# CORS
CORS_ORIGINS=http://localhost:3000
```

## Running the Application

### Development Mode

```bash
python app.py
```

Or using Flask CLI:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

The API will be available at `http://localhost:5000`

### Production Mode

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

## API Endpoints

### Health Check
- `GET /api/health` - Check API status

### A1 Cutting Process
- `POST /api/a1/submit` - Submit A1 feedback form
- `GET /api/a1/history` - Get A1 history
- `GET /api/a1/history/download` - Download A1 history as Excel

### GHM Cutting Process
- `POST /api/ghm/submit` - Submit GHM feedback form
- `GET /api/ghm/history` - Get GHM history
- `GET /api/ghm/history/download` - Download GHM history as Excel

### KEM Cutting Process
- `POST /api/kem/submit` - Submit KEM feedback form
- `GET /api/kem/history` - Get KEM history
- `GET /api/kem/history/download` - Download KEM history as Excel

See `API_TESTING.md` for detailed API documentation and examples.

## Email Configuration

Email recipient lists are configured in `config.py`. Update the following lists as needed:

- `EMAIL_RECIPIENTS_A1`
- `EMAIL_RECIPIENTS_GHM`
- `EMAIL_RECIPIENTS_KEM`

## File Storage

Uploaded files are stored in:
- `uploads/a1/` - A1 form uploads
- `uploads/ghm/` - GHM form uploads
- `uploads/kem/` - KEM form uploads

Grid images are also stored in these directories.

## Excel History Files

History is stored in Excel files in the project root:
- `history_A1.xlsx`
- `history_GHM.xlsx`
- `history_KEM.xlsx`

These files are created automatically if they don't exist.

## Logging

Logs are written to `logs/cutting_feedback.log` in production mode.

## Testing

Test the API using curl or Postman. See `API_TESTING.md` for examples.

Example:

```bash
curl http://localhost:5000/api/health
```

## Troubleshooting

### Email not sending
- Check email server configuration in `.env`
- Verify network connectivity to mail server
- Check logs for error messages

### File upload fails
- Check file size limits in configuration
- Verify upload directory permissions
- Check allowed file extensions

### Excel operations fail
- Ensure openpyxl is installed
- Check file permissions for history Excel files
- Verify file paths in configuration

## Security Considerations

- Change `SECRET_KEY` in production
- Configure CORS origins appropriately
- Implement authentication if needed
- Add rate limiting for production
- Validate and sanitize all inputs
- Use HTTPS in production

## License

Internal use only.



