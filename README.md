# PDF Merger Application

A simple web application to merge PDF files with automatic page numbering and blank page insertion.

## Features

- **Multiple PDF Upload**: Select and upload multiple PDF files at once
- **Order Preservation**: PDFs are merged in the order you select them
- **Automatic Page Numbering**: Adds page numbers to the bottom right corner of each page
- **Blank Page Insertion**: Automatically adds a blank page after any PDF with an odd number of pages
- **Front Page Alignment**: Ensures each new PDF starts on the front of a page (perfect for duplex printing)

## Setup

1. Make sure you're in the project directory:
   ```bash
   cd ~/projects/PDF-Merger
   ```

2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Activate the virtual environment (if not already activated):
   ```bash
   source .venv/bin/activate
   ```

2. Run the Flask application:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. Click the upload area or drag and drop PDF files
2. Select multiple PDFs (they will be merged in selection order)
3. Review the file list to confirm order
4. Click "Merge PDFs" button
5. Wait for processing to complete
6. Download your merged, numbered PDF

## How It Works

1. **Upload**: You upload multiple PDF files through the web interface
2. **Merge**: The application merges the PDFs in order
3. **Blank Pages**: After each PDF with an odd number of pages, a blank page is inserted
4. **Numbering**: Page numbers are added to the bottom right corner of every page
5. **Download**: The final merged PDF is available for download

## File Structure

```
PDF-Merger/
├── app.py                      # Flask application
├── templates/
│   └── index.html             # Web interface
├── uploads/                   # Temporary upload storage
├── output/                    # Processed PDF output
├── Blank PDF Document.pdf     # Blank page template
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Requirements

- Python 3.8+
- Flask
- PyPDF2
- reportlab
- werkzeug

## Notes

- Maximum file size: 50MB per upload
- Only PDF files are accepted
- Uploaded files are temporarily stored and cleaned on each new upload
- The blank page ensures proper alignment for duplex printing
