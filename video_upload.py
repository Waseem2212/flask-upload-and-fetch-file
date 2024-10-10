from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ensure the upload forler exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS_VIDEO = {'mp4','mkv'}
def allowed_file(filename,allowed_extensions):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed_extensions 

@app.route('/upload/video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error':'file not exists'}),400
    file = request.files('file')
    if file.filename == '':
        return jsonify({'error':'File not select'}),400
    
    # agr video ha
    if allowed_file(file.filename,ALLOWED_EXTENSIONS_VIDEO):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(file_path)
    
        # video duration
        video = VideoFileClip(file_path)
        duration = video.duration
        return jsonify({'message':'Video processed','duration':duration})

    return jsonify({'error':'Unsupported file type'}),400

if __name__ == '__main__':
    app.run(debug=True,port=8282)
