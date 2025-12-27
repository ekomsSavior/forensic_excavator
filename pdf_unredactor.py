import fitz
import os

def extract_pdf_text(pdf_path, output_dir):
    """
    Extract all text objects from a PDF, including improperly redacted content.
    """
    os.makedirs(output_dir, exist_ok=True)

    base = os.path.basename(pdf_path)
    name = os.path.splitext(base)[0]
    output_path = os.path.join(output_dir, f"{name}.unredacted.txt")

    doc = fitz.open(pdf_path)
    extracted = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        extracted.append(f"\n--- Page {page_num + 1} ---\n{text}")

    doc.close()

    full_text = "\n".join(extracted)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    return output_path, len(full_text)
