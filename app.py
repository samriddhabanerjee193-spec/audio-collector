import os
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Set target word to OCTOPUS and duration to 1 second
TARGET_WORD = "OCTOPUS"
MAX_DURATION_SECONDS = 1

# Local directory to temporarily save recorded audio blobs
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template(
        'index.html', 
        target_word=TARGET_WORD, 
        max_duration=MAX_DURATION_SECONDS
    )

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Extract word label from custom header
        word_label = request.headers.get('X-Word-Label', 'UNKNOWN').upper()
        
        # Read raw binary audio payload from client
        audio_data = request.data
        if not audio_data:
            return jsonify({'error': 'No audio data received'}), 400

        # Create unique timestamped filename
        timestamp = int(time.time() * 1000)
        filename = f"{word_label}_{timestamp}.webm"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Write audio binary to file
        with open(file_path, 'wb') as f:
            f.write(audio_data)

        return jsonify({'message': 'File uploaded successfully', 'file': filename}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)