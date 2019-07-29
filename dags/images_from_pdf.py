from pdflib import Document
import os

doc = Document('PDFs/US20190029958.pdf')

for page in doc:
    page.extract_images(path='temp/images', prefix='img')
