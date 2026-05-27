import os
import fitz

import pytesseract

from PIL import Image
from docx import Document
from pdf2image import convert_from_path



pytesseract.pytesseract.tesseract_cmd = (
    r'C:\Program Files\Tesseract-OCR\tesseract.exe'
)


def extract_text(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    # IMAGE FILES
    if extension in ['.png', '.jpg', '.jpeg']:

        try:

            image = Image.open(file_path)

            text = pytesseract.image_to_string(
                image
            )

            return text

        except:

            return ""

    # PDF FILES
    elif extension == '.pdf':

        text = ""

        try:

            pdf = fitz.open(file_path)

            for page in pdf:

                text += page.get_text()

            return text

        except:

            return ""

    # DOCX FILES
    elif extension == '.docx':

        try:

            doc = Document(file_path)

            text = ""

            for para in doc.paragraphs:

                text += para.text + "\n"

            return text

        except:

            return ""

    # TXT FILES
    elif extension == '.txt':

        try:

            with open(
                file_path,
                'r',
                encoding='utf-8'
            ) as file:

                return file.read()

        except:

            return ""

    return ""