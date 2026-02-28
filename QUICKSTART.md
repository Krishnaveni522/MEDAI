# MedAI - Quick Start Guide

## Step 1: Install Dependencies

Open PowerShell in the medai folder and run:

```powershell
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- python-docx (for DOCX file processing)
- EasyOCR (advanced OCR engine)
- Pytesseract (OCR fallback)
- Pillow (image processing)
- Other required libraries

## Step 2: Install Tesseract OCR

1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer
3. Install to: `C:\Program Files\Tesseract-OCR\`
4. Verify installation by running: `tesseract --version`

## Step 3: Run the Application

Navigate to the src directory and start the Flask server:

```powershell
cd src
python app.py
```

You should see output like:
```
* Running on http://127.0.0.1:5000
* Restarting with stat
* Debugger is active!
```

## Step 4: Open in Browser

Open your web browser and go to:
```
http://localhost:5000
```

## Using the Application

### Admin Portal (First Time Setup)

1. Click **"Admin"** on the home page
2. You'll see three sections:
   - **Import from DOCX**: Upload your Drug_Information.docx file
   - **Register New Medicine**: Add medicines manually
   - **Medicine Database**: View all medicines

3. **Option A - Import from DOCX**:
   - Click "Choose File"
   - Select your `Drug_Information.docx` file
   - Click "Upload & Import"
   - All medicines will be added to the database

4. **Option B - Add Manually**:
   - Enter the drug name (e.g., "Aspirin")
   - Enter the instructions (e.g., "Take 1 tablet with water after meals...")
   - Click "Add Medicine"

### Patient Portal

1. Click **"Patient"** on the home page
2. Take a clear photo of a medicine label or upload an existing image
3. Click "Choose File" or drag and drop the image
4. Click "Upload & Analyze"
5. Wait for OCR processing (5-25 seconds)
6. View the results:
   - Matched medicine names
   - Confidence scores
   - Complete instructions

## Tips for Best Results

### For Admin:
- Upload comprehensive drug information in DOCX format first
- Keep drug names consistent (use both generic and brand names)
- Include detailed instructions with dosage information

### For Patients:
- Take photos in good lighting
- Keep the camera steady (avoid blurry images)
- Capture the medicine label clearly
- Include brand name and generic name if visible
- Try multiple angles if first attempt doesn't work

## Troubleshooting

### "No text could be extracted"
- Image may be too blurry
- Lighting is poor
- Text is too small
- Try taking another photo in better lighting

### "No matching medicines found"
- The medicine might not be in the database yet
- OCR may have misread the label
- Check the "Extracted Text" section to see what was detected
- Admin needs to add this medicine to the database

### Application won't start
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 5000 is already in use
- Try using a different port: `python app.py` and edit the port in app.py

### Import DOCX not working
- Make sure the file is in .docx format (not .doc)
- Check the file format matches the guide in DOCX_FORMAT_GUIDE.md
- Ensure drug names and instructions are clearly separated

## Default Database Location

The SQLite database is created automatically at:
```
medai/src/drug_information.db
```

You can view/edit it using:
- DB Browser for SQLite
- Any SQLite management tool
- Or through the Admin portal interface

## Security Note

⚠️ **Important**: Before deploying to production:
1. Change the `app.secret_key` in `app.py`
2. Add user authentication for the admin portal
3. Use HTTPS instead of HTTP
4. Implement rate limiting
5. Add input validation and sanitization

## Support

For issues or questions:
1. Check the README.md file
2. Review the DOCX_FORMAT_GUIDE.md for file format help
3. Check the console output for error messages
4. Verify all dependencies are correctly installed

## What's Next?

After setting up:
1. ✅ Populate the database with common medicines
2. ✅ Test with sample medicine images
3. ✅ Customize the styling if needed
4. ✅ Add more medicines as needed
5. ✅ Train staff/users on how to use the system

---

**Remember**: This application is for informational purposes only. Always consult healthcare professionals for medical advice.
