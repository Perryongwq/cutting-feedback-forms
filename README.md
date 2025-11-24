# Cutting Process Feedback Application

A full-stack application for managing cutting process feedback with Flask REST API backend and React frontend.

## Overview

This application allows users to submit cutting process feedback through three different forms (A1, GHM, KEM), send emails with attachments, and maintain history in Excel files.

## Architecture

- **Backend**: Flask REST API (Python)
- **Frontend**: React (JavaScript)
- **Database**: Excel files (history storage)
- **Email**: Flask-Mail

## Project Structure

```
cutting-feedback-form/
├── backend/          # Flask API
│   ├── app.py
│   ├── config.py
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── utils/
├── frontend/        # React app
│   ├── public/
│   ├── src/
│   └── package.json
├── history_*.xlsx   # History files
└── README.md
```

## Quick Start

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. Run backend:
   ```bash
   python app.py
   ```

Backend runs on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run frontend:
   ```bash
   npm start
   ```

Frontend runs on `http://localhost:3000`

## Features

- **Three Feedback Forms**: A1, GHM, KEM cutting process feedback
- **Interactive Grids**: 6x6 grid for A1, 3x3 for GHM/KEM
- **File Uploads**: Multiple image uploads with validation
- **Email Notifications**: Automatic email with form data and attachments
- **History Management**: View and download history as Excel
- **Form Validation**: Client and server-side validation
- **Responsive Design**: Works on desktop and mobile

## API Documentation

See `backend/API_TESTING.md` for detailed API documentation and testing examples.

## Configuration

### Backend

Edit `backend/.env`:
- Email server settings
- File upload limits
- CORS origins

### Frontend

Edit `frontend/.env` (optional):
- API URL (defaults to `http://localhost:5000/api`)

## Deployment

### Backend

For production, use Gunicorn:

```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

### Frontend

Build for production:

```bash
cd frontend
npm run build
```

Serve the `build/` directory with a web server like Nginx.

## Docker (Optional)

See `docker-compose.yml` for containerized deployment.

## Troubleshooting

### Backend Issues
- Check `.env` configuration
- Verify email server connectivity
- Check file permissions for uploads and history files
- Review logs in `backend/logs/`

### Frontend Issues
- Verify backend is running
- Check API URL configuration
- Review browser console for errors
- Clear browser cache

## Development

### Adding New Features

1. **Backend**: Add routes in `backend/routes/`, services in `backend/services/`
2. **Frontend**: Add components in `frontend/src/components/`, update `App.js` for routing

### Testing

- Backend: Use curl or Postman (see `backend/API_TESTING.md`)
- Frontend: Manual testing in browser

## License

Internal use only.

## Support

For issues or questions, contact the development team.
