import easyocr
import camelot
import json
from pdf2image import convert_from_path
import sys
import os

def process_pdf(file_path):
    tables = []

    # Convert PDF pages to images
    images = convert_from_path(file_path)
    reader = easyocr.Reader(['en'])

    for img in images:
        # Attempt to extract tables using Camelot
        camelot_tables = camelot.read_pdf(file_path, flavor='stream')

        for table in camelot_tables:
            table_data = table.df.to_dict()  # Convert to dictionary
            tables.append(table_data)

    return tables

if __name__ == "__main__":
    file_path = sys.argv[1]
    tables = process_pdf(file_path)
    print(json.dumps(tables))
