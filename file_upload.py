from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document,doc

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ensure the upload forler exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS_PDF = {'pdf','docx'}
ALLOWED_EXTENSIONS_DOCX = {'docx'}
 # file extension check krny k liye
def allowed_file(filename,allowed_extensions):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed_extensions

@app.route('/upload/file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error':'file not exists'}),400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error':'file not select'}),400
    
    # agar pdf file ha
    if allowed_file(file.filename, ALLOWED_EXTENSIONS_PDF):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(file_path)
        # pdf se text extract karna
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return jsonify({'message':'PDF processed','text':text})
    
    elif allowed_file(file.filename, ALLOWED_EXTENSIONS_DOCX):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)

        # docx se text extract krna
        text = '\n'.join([para.text for para in doc.paragraphs])
        return jsonify({'message':'word file processed','text': text})
    

    return jsonify({'error':'unsupported file type'}),400

if __name__ == '__main__':
    app.run(debug=True,port=8000)

