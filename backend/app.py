import pdfplumber
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/extract-data": {"origins": "http://localhost:3000"}})

@app.route('/extract-data', methods=['POST'])
def extract_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        tables = []
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                # Extract tables normally
                extracted_tables = page.extract_tables()
                
                # Extract tables from the left side of the page
                left_half = page.within_bbox((0, 0, page.width / 2, page.height))
                left_tables = left_half.extract_tables()

                # Combine tables from both extractions
                all_tables = extracted_tables + left_tables

                # Process the extracted tables
                for table in all_tables:
                    # Skip malformed tables
                    if len(table) < 2 or len(table[0]) < 1:
                        print(f"Table on page {pdf.pages.index(page) + 1} is malformed.")
                        continue

                    # Identify headers and data more robustly
                    # Assume the first row is headers if it's a proper header length
                    if all(isinstance(x, str) for x in table[0]):
                        headers = table[0]
                        data = table[1:]
                    else:
                        headers = table[1]  # Fallback if first row isn't strings
                        data = table[2:]

                    df = pd.DataFrame(data, columns=headers)  # Use identified headers
                    # Clean data by removing empty columns or rows
                    df.dropna(axis=1, how='all', inplace=True)  # Remove empty columns
                    df.dropna(axis=0, how='all', inplace=True)  # Remove empty rows

                    # Additional cleaning: removing extra spaces
                    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

                    tables.append({"headers": headers, "data": df.values.tolist()})
                else:
                    print(f"No tables found on page {pdf.pages.index(page) + 1}")

        return jsonify({"data": tables})

    except Exception as e:
        print(f"Error processing file: {e}")  # Log the error for debugging
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
