# Quick Start Guide

## Installation

1. Navigate to the project:
   ```bash
   cd ~/projects/PDF-Merger
   ```

2. Activate virtual environment:
   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the Application

**Option 1: Using the run script (easiest)**
```bash
./run.sh
```

**Option 2: Manual**
```bash
source .venv/bin/activate
python app.py
```

Then open your browser to: **http://localhost:5000**

## Quick Test

1. Visit http://localhost:5000
2. Click the upload area
3. Select 2-3 PDF files (in the order you want them merged)
4. Click "Merge PDFs"
5. Download your merged, numbered PDF

The application will:
- Merge PDFs in selection order
- Add blank pages after odd-page PDFs
- Number all pages in the bottom right corner
