import cv2
import fitz
import numpy as np
from PIL import Image


def scan_qr(image_path):

    detector = cv2.QRCodeDetector()

    image = cv2.imread(image_path)

    data, bbox, _ = detector.detectAndDecode(image)

    return data


def extract_qr_from_pdf(pdf_path):

    detector = cv2.QRCodeDetector()

    pdf = fitz.open(pdf_path)

    for page_num in range(len(pdf)):

        page = pdf[page_num]

        pix = page.get_pixmap()

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        img_np = np.array(img)

        data, bbox, _ = detector.detectAndDecode(img_np)

        if data:

            return data

    return None