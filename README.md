# MedAI - Medical Instructions Application

A Flask-based web application for managing and retrieving medicine instructions using OCR technology.

## Features

### Home Page
- Clean interface with two main sections: **Patient** and **Admin**
- Easy navigation to both portals

### Admin Portal
- **Upload Drug Information**: Import medicine data from `Drug_Information.docx` file
- **View All Medicines**: Display all medicines in a searchable table with columns:
  - Drug name
  - Instructions
- **Register New Medicine**: Manually add new medicines with a simple form
- **Edit/Delete**: Update or remove existing medicine entries
- **Database Management**: All data stored in SQLite database

### Patient Portal
- **Upload Medicine Label Photo**: Patients can upload photos of medicine labels in any orientation
- **Advanced OCR**: Uses EasyOCR (with Tesseract fallback) for accurate text extraction
- **Smart Matching**: Intelligently matches extracted text with database entries
- **Display Results**: Shows matching medicines with:
  - Medicine name
  - Instructions
  - Confidence score
  - Matched variant information

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **OCR Engine**: EasyOCR (primary), Pytesseract (fallback)
- **Document Processing**: python-docx
- **Frontend**: HTML, CSS, Bootstrap 4, JavaScript
- **Image Processing**: Pillow (PIL)

## Installation

1. **Clone the repository**
   ```bash
   cd c:\Users\Asus\Downloads\kvfinaloutput\medai
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR** (if not already installed)
   - Download from: https://github.com/tesseract-ocr/tesseract
   - Install to: `C:\Program Files\Tesseract-OCR\`

4. **Prepare Drug Information File**
   - Create a DOCX file with a table containing two columns:
     - Column 1: Drug name
     - Column 2: Instructions

## Running the Application

1. Navigate to the src directory:
   ```bash
   cd src
   ```

2. Run the Flask application:
   ```bash
   python app.py
   ```

3. Open your browser and go to:
   ```
   http://localhost:5000
   ```

## Usage

### For Administrators

1. Click on **Admin** from the home page
2. **Upload DOCX**: Select and upload your `Drug_Information.docx` file
3. **Add Manually**: Use the form to register new medicines one by one
4. **Manage Database**: Edit or delete existing entries as needed

### For Patients

1. Click on **Patient** from the home page
2. Upload a clear photo of the medicine label
3. Wait for OCR processing
4. View matched medicine instructions and details

## File Structure

```
medai/
├── src/
│   ├── app.py                 # Main Flask application
│   ├── templates/
│   │   ├── index.html         # Home page
│   │   ├── admin.html         # Admin portal
│   │   ├── patient.html       # Patient upload page
│   │   └── results.html       # Search results page
│   ├── utils/
│   │   ├── database.py        # Database operations
│   │   └── ocr_easyocr.py     # OCR processing
│   ├── uploads/               # Temporary file storage
│   └── drug_information.db    # SQLite database (auto-created)
└── requirements.txt           # Python dependencies
```

## Database Schema

### drug_information table
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `drug` (TEXT, NOT NULL, UNIQUE)
- `instructions` (TEXT, NOT NULL)
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

## API Endpoints

- `GET /` - Home page
- `GET /patient` - Patient upload page
- `POST /patient/upload` - Process uploaded medicine image
- `GET /admin` - Admin portal
- `POST /admin/add` - Add new medicine
- `POST /admin/update` - Update existing medicine
- `POST /admin/delete` - Delete medicine
- `POST /admin/import-docx` - Import from DOCX file
- `GET /api/database` - Get all medicines as JSON (debugging)

## OCR Features

- **Multi-orientation support**: Handles images in any rotation
- **Smart preprocessing**: Automatic image enhancement for better accuracy
- **Dual OCR engines**: EasyOCR for primary processing, Tesseract as fallback
- **Intelligent matching**: Uses fuzzy matching algorithms to find medicines even with OCR errors

## Notes

- Maximum file upload size: 10MB
- Supported image formats: PNG, JPG, JPEG
- Supported document format: DOCX
- OCR processing time: 5-25 seconds depending on image quality

## Security Considerations

- Change the `app.secret_key` in production
- Implement user authentication for admin portal
- Add input validation and sanitization
- Use HTTPS in production

## Future Enhancements

- User authentication and role-based access
- Search functionality in admin portal
- Batch medicine upload
- Export database to Excel/CSV
- Multi-language support
- Medicine image library
- Dosage calculator

## License

This project is for educational and healthcare assistance purposes.

## Disclaimer

This application is for informational purposes only. Always consult with healthcare professionals before taking any medication.
