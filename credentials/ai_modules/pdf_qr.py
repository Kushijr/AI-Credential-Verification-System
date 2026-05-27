import cv2

from pdf2image import convert_from_path


def extract_qr_from_pdf(pdf_path):

    pages = convert_from_path(pdf_path)

    detector = cv2.QRCodeDetector()

    for i, page in enumerate(pages):

        temp_image = f"temp_page_{i}.png"

        page.save(temp_image, "PNG")

        image = cv2.imread(temp_image)

        data, bbox, _ = detector.detectAndDecode(image)

        if data:

            return data

    return None