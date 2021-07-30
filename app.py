import os
from flask import Flask, redirect, render_template, url_for, request
from PIL import Image
from ocr import ocr_core


# folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)


# function to check the file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('home.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('home.html', msg='No file selected')

        if file and allowed_file(file.filename):

            # call the OCR function on it
            extracted_text = ocr_core(file)
            extracted_info = localise_text_tesseract(file)
            size = 500, 500
            with Image.open(file) as im:
                im.thumbnail(size, Image.ANTIALIAS)
                im.save('static/uploads/' + file.filename)
            # extract the text and display it
            return render_template('home.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/features')
def features():
    return render_template('features.html', title='Features')


if __name__ == '__main__':
    app.run(debug=True)