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
                extracted_tables = page.extract_tables()
                
                # Check if any tables were found
                if extracted_tables:
                    for table in extracted_tables:
                        df = pd.DataFrame(table[1:], columns=table[0])  # Use first row as header
                        # Optional: Clean data by removing empty columns or rows
                        df.dropna(axis=1, how='all', inplace=True)  # Remove empty columns
                        df.dropna(axis=0, how='all', inplace=True)  # Remove empty rows
                        tables.append({"headers": table[0], "data": df.values.tolist()})
                else:
                    print(f"No tables found on page {pdf.pages.index(page) + 1}")

        return jsonify({"data": tables})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
