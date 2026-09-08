import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Target word and recording duration settings
TARGET_WORD = "OCTOPUS"
MAX_DURATION_SECONDS = 1

@app.route('/')
def index():
    return render_template(
        'index.html', 
        target_word=TARGET_WORD, 
        max_duration=MAX_DURATION_SECONDS
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)