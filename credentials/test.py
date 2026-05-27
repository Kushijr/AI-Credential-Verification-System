from ai_modules.ocr import extract_text

text = extract_text('../sample_certificate.png')

print(text)