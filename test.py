import os
from flask import Flask, render_template, request, redirect, url_for, flash, session 
from werkzeug.utils import secure_filename
app = Flask(__name__)

# ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # if request.method == 'POST':
    #     # check if the postgit  request has the file part
    #     if 'file' not in request.files:
    #         return render_template('index.html', error='No file part')

    #     file = request.files['file']

    #     # if user does not select file, browser also
    #     # submit an empty part without filename
    #     if file.filename == '':
    #         return render_template('index.html', error='No selected file')

    #     # Save the file to the desired location
    #     filename = secure_filename(file.filename)
    #     file.save(os.path.join('uploads/', filename))

    #     return render_template('index.html', success='File successfully uploaded')
    print("Hello Worldrvebtbrynet5yjmemmemu")
    return render_template('index.html')
def hello_world():
    print("Hello World")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)