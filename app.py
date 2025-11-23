from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
from pathlib import Path
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

BLANK_PDF_PATH = 'Blank PDF Document.pdf'

def add_page_numbers(pdf_path, output_path):
    """Add page numbers to the bottom right corner of each page."""
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        
        # Create a new PDF with just the page number
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        
        # Get page dimensions
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        
        # Position for bottom right (with some margin)
        x_position = page_width - 50
        y_position = 30
        
        # Draw page number
        can.setFont("Helvetica", 10)
        can.drawString(x_position, y_position, str(page_num + 1))
        can.save()
        
        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        number_pdf = PdfReader(packet)
        
        # Merge the page number onto the original page
        page.merge_page(number_pdf.pages[0])
        writer.add_page(page)
    
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

def merge_pdfs_with_blanks(pdf_files):
    """
    Merge PDFs, adding a blank page after any PDF with odd page count.
    """
    merger = PdfMerger()
    blank_reader = PdfReader(BLANK_PDF_PATH)
    
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        page_count = len(reader.pages)
        
        # Add all pages from the PDF
        merger.append(pdf_file)
        
        # If odd number of pages, add a blank page
        if page_count % 2 == 1:
            merger.append(BLANK_PDF_PATH, pages=(0, 1))  # Add just the first page
    
    return merger

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files[]')
    
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    # Clear previous uploads
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
    
    uploaded_files = []
    first_filename = None
    for file in files:
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            if first_filename is None:
                first_filename = filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_files.append(filepath)
    
    if not uploaded_files:
        return jsonify({'error': 'No valid PDF files'}), 400
    
    # Generate output filename based on first file
    base_name = os.path.splitext(first_filename)[0]
    output_filename = f"{base_name}-merged.pdf"
    
    try:
        # Merge PDFs with blank pages
        merger = merge_pdfs_with_blanks(uploaded_files)
        
        # Save merged PDF temporarily
        temp_merged = os.path.join(app.config['OUTPUT_FOLDER'], 'temp_merged.pdf')
        with open(temp_merged, 'wb') as output_file:
            merger.write(output_file)
        merger.close()
        
        # Add page numbers to the merged PDF
        final_output = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        add_page_numbers(temp_merged, final_output)
        
        # Clean up temp file
        os.remove(temp_merged)
        
        return jsonify({
            'success': True,
            'message': f'Successfully merged {len(uploaded_files)} PDFs',
            'download_url': '/download',
            'filename': output_filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download')
def download_file():
    # Get the filename from query parameter, or use default
    filename = request.args.get('filename', 'merged_output.pdf')
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True, download_name=filename)
    return jsonify({'error': 'No file available'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)