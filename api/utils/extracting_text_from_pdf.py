
from api.ai_logics.ai_connection_function import generate
import fitz  # PyMuPDF
import io
from PIL import Image
import pytesseract
import re
from fpdf import FPDF


# for extracting text from files
def extract_info_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    results = []

    for page_number, page in enumerate(doc):
        page_info = {
            "page_number": page_number + 1,
            "text": "",
            "images": []
        }

        # Extract page text
        text = page.get_text()
        page_info["text"] = text.strip()

        # Extract and OCR images
        images = page.get_images(full=True)
        for img in images:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))

            # OCR on the image
            extracted_text = pytesseract.image_to_string(image).strip()
            page_info["images"].append(extracted_text)

        results.append(page_info)

    doc.close()
    return results


#for getting joined text taken from extract_info_from_pdf
def all_question_joined_from_file(file_path:list):
    file_text = extract_info_from_pdf(file_path)
    all_text = "\n".join(page["text"] for page in file_text)
    return all_text
    
    
#for seperating questions one by one
def extract_individual_questions(text) -> list:
    # Split where a question starts (e.g., '1.' or '12.')
    question_parts = re.split(r'\n(?=\d{1,2}[\.])', text)
    questions = []
    for part in question_parts:
        cleaned = part.strip()
        if cleaned:
            questions.append(cleaned)
    return questions


def grouping_questions(lst:list,group_member_number):
    all_lst = [lst[i:i+group_member_number] for i in range(0,len(lst),group_member_number)]
    return all_lst


