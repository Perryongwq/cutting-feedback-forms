# Cutting Process Feedback - Frontend

React frontend application for the Cutting Process Feedback system.

## Features

- Three feedback forms: A1, GHM, KEM
- Interactive grid selector (6x6 for A1, 3x3 for GHM/KEM)
- Multiple file upload with preview
- Form validation
- History table with sorting and filtering
- Excel download functionality
- Toast notifications
- Responsive design

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── App.js              # Main app component
│   ├── index.js            # Entry point
│   ├── components/
│   │   ├── Layout/        # Layout components
│   │   ├── Forms/          # Form components
│   │   ├── Grid/           # Grid selector
│   │   ├── Common/         # Reusable components
│   │   └── History/        # History components
│   └── services/
│       └── api.js          # API service layer
└── package.json
```

## Prerequisites

- Node.js 14+ and npm
- Backend API running (see backend README)

## Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure API URL (optional):**
   
   Create `.env` file in frontend directory:
   ```env
   REACT_APP_API_URL=http://localhost:5000/api
   ```
   
   If not set, defaults to `http://localhost:5000/api`

## Running the Application

### Development Mode

```bash
npm start
```

The app will open at `http://localhost:3000`

### Production Build

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## Usage

1. **Select a form** from the sidebar (A1, GHM, or KEM)
2. **Fill in all required fields**
3. **Select grid cells** by clicking on them
4. **Upload photos** (at least one required)
5. **Click "Send Email"** to submit
6. **View history** in the Summary History section
7. **Download history** as Excel using the download button

## Components

### Layout Components
- **Sidebar**: Navigation between forms
- **Header**: Page title

### Form Components
- **A1Form**: A1 cutting process feedback form
- **GHMForm**: GHM cutting feedback form
- **KEMForm**: KEM cutting feedback form

### Common Components
- **FileUpload**: Multiple file upload with drag & drop
- **DateTimePicker**: Date and time input
- **MultiSelect**: Multi-select dropdown

### Grid Components
- **GridSelector**: Interactive grid (6x6 or 3x3)
- **GridCell**: Individual grid cell

### History Components
- **HistoryTable**: Sortable and filterable history table
- **DownloadButton**: Download history as Excel

## Form Validation

All forms include client-side validation:
- Required fields
- Lot number max length (10 chars for A1 and KEM)
- File type validation (jpg, jpeg, png only)
- At least one photo required

## API Integration

The frontend communicates with the backend API through the `services/api.js` module. All API calls use axios with error handling and interceptors.

## Styling

- CSS modules for component-specific styles
- Global styles in `App.css` and `index.css`
- Responsive design with flexbox

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### API connection fails
- Verify backend is running
- Check API URL in `.env`
- Check CORS configuration in backend

### Forms not submitting
- Check browser console for errors
- Verify all required fields are filled
- Check file uploads are valid images

### History not loading
- Check API endpoint is accessible
- Verify backend is running
- Check browser console for errors

## Development

### Adding a new form

1. Create new form component in `components/Forms/`
2. Add route in `App.js`
3. Add menu item in `Sidebar.jsx`
4. Create API service methods in `services/api.js`
5. Add backend routes (see backend README)

### Customizing styles

Edit component CSS files or `App.css` for global styles.

## License

Internal use only.



