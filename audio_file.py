from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import speech_recognition as sr

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ensure the upload forler exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename,allowed_extensions):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed_extensions 

ALLOWED_EXTENSIONS_AUDIO = {'wav','mp3'}

@app.route('/upload/audio',methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({'error':'file not exists'}),400
    file = request.files('file')
    if file.filename == '':
        return jsonify({'error':'File not select'}),400
    
    # agr audio file ho
    if allowed_file(file.filename,ALLOWED_EXTENSIONS_AUDIO):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(file_path)

# speech recognition se audio ko text mein convert karay
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google_cloud(audio)
            return jsonify({'message':'Audio processed','text': text})
        except sr.UnknownValueError:
            return jsonify({'error':'Audio not clear'}),400
        except sr.RequestError:
            return jsonify({'error':'Speech recognition error'}),500
    return jsonify({'error':'Unsupported file type'}),400
    


if __name__ == '__main__':
    app.run(debug=True,port=8181)