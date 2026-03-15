import argparse
import concurrent.futures
import io
import os

import fitz  # PyMuPDF
from PIL import Image, ImageFilter


def upscale_pdf(input_path, output_path, scale_factor=2):
    doc = fitz.open(input_path)
    new_doc = fitz.open()  # Create a new PDF

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        images = page.get_images(full=True)

        if images:
            # Assuming one image per page
            img_info = images[0]
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # Open with PIL
            img = Image.open(io.BytesIO(image_bytes))

            # Upscale with high-quality resampling
            new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
            upscaled_img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Sharpen the upscaled image
            upscaled_img = upscaled_img.filter(
                ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3)
            )

            # Convert back to bytes with optimized quality
            img_buffer = io.BytesIO()
            if image_ext.upper() == "JPEG":
                upscaled_img.save(
                    img_buffer, format=image_ext.upper(), quality=80, optimize=True
                )
            else:
                upscaled_img.save(img_buffer, format=image_ext.upper())
            upscaled_bytes = img_buffer.getvalue()

            # Create new page with upscaled image
            new_page = new_doc.new_page(
                width=upscaled_img.width, height=upscaled_img.height
            )
            new_page.insert_image(
                fitz.Rect(0, 0, upscaled_img.width, upscaled_img.height),
                stream=upscaled_bytes,
            )

    new_doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    new_doc.close()


def main(num_workers=2):
    input_dir = "data"
    output_dir = "out"
    os.makedirs(output_dir, exist_ok=True)

    pdf_files = [
        filename
        for filename in os.listdir(input_dir)
        if filename.lower().endswith(".pdf")
    ]

    def process_file(filename):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"upscaled_{filename}")
        print(f"Processing {filename}...")
        upscale_pdf(input_path, output_path)
        print(f"Saved to {output_path}")

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        executor.map(process_file, pdf_files)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upscale PDFs in parallel.")
    parser.add_argument(
        "--workers", type=int, default=2, help="Number of parallel workers (default: 2)"
    )
    args = parser.parse_args()
    main(num_workers=args.workers)
