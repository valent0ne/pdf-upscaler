# PDF Upscaler

A Python script to upscale PDF files by enhancing the resolution of images within them. Particularly useful for scanned documents or PDFs with low-resolution images.

## Features

- Extracts images from PDF pages
- Upscales images by 2x using high-quality Lanczos resampling
- Applies sharpening for enhanced clarity
- Optimizes output size with JPEG compression and PDF deflate
- Processes all PDFs in `data/` directory automatically

## Requirements

- Python 3.12 or higher
- Virtual environment (recommended)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/valent0ne/pdf-upscaler.git
   cd pdf-upscaler
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your PDF files in the `data/` directory.
2. Run the script:

   ```bash
   python upscale_pdf.py
   ```

3. Find the upscaled PDFs in the `out/` directory with "upscaled_" prefix.

## How it works

The script assumes each page of the PDF contains a single image (typical for scanned documents). It:

1. Extracts images from each PDF page using PyMuPDF
2. Resizes images to double resolution with Lanczos resampling
3. Applies unsharp mask sharpening for better clarity
4. Recreates the PDF with optimized JPEG quality (80%) and compression

## Limitations

- Designed for PDFs with one image per page
- May not preserve complex layouts with text and multiple images
- Output file size increases with higher resolution
