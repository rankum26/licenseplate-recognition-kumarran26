import os
import sys
from flask import Flask, request, render_template, send_from_directory


sys.path.append(os.path.join(os.path.dirname(__file__), 'detection'))

import main

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        # create Run-folder
        run_folder = main.get_next_run_folder()
        os.makedirs(run_folder, exist_ok=True)

        # save image to Run-folder
        file_path = os.path.join(run_folder, file.filename)
        file.save(file_path)

        # Process the image
        results, detected, output_paths = main.process_image(file_path, run_folder)

        return render_template('result.html', result=results, detected=detected, output_paths=output_paths)

@app.route('/runs_done/<path:filename>')
def send_file(filename):
    return send_from_directory('runs_done', filename)

if __name__ == "__main__":
    app.run(debug=True)
