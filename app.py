from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
import os
import uuid

app = Flask(__name__)
app.secret_key = 'nahipata'  # Replace with your secret key

# Configuration
UPLOAD_FOLDER = 'static/uploads/'
CONVERTED_FOLDER = 'static/converted/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Ensure upload and converted directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Secure the filename and generate a unique filename
            filename = secure_filename(file.filename)
            unique_filename = str(uuid.uuid4()) + "_" + filename
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(upload_path)

            # Open the image to detect its format
            try:
                with Image.open(upload_path) as img:
                    original_format = img.format.lower()
            except Exception as e:
                flash('Uploaded file is not a valid image.')
                return redirect(request.url)

            # Get desired format from form
            desired_format = request.form.get('format')
            if not desired_format:
                flash('No target format selected.')
                return redirect(request.url)

            # Convert the image
            converted_filename = f"{uuid.uuid4()}_{os.path.splitext(filename)[0]}.{desired_format}"
            converted_path = os.path.join(app.config['CONVERTED_FOLDER'], converted_filename)

            try:
                with Image.open(upload_path) as img:
                    # Convert and save the image
                    img = img.convert('RGB') if desired_format in ['jpg', 'jpeg'] else img
                    img.save(converted_path, desired_format.upper())
            except Exception as e:
                flash('Error converting image.')
                return redirect(request.url)

            return render_template('result.html', original_image=upload_path, converted_image=converted_path, converted_filename=converted_filename)

        else:
            flash('Allowed image types are png, jpg, jpeg, gif, bmp, tiff.')
            return redirect(request.url)

    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['CONVERTED_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
