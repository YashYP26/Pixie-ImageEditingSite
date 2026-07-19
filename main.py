from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = "my_super_secret_key_123"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def imageProcessing(filename, operation):
    print(f"The operation is {operation} and The filename is {filename}")
    image = cv2.imread(f"uploads/{filename}")
    if image is None:
        print("Image not loaded!")
        return None

    match operation :
        case "grayscale":
            processedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(f"static/{filename}", processedImage)
            return filename
        case "sketch":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            invert = 255 - gray
            blur = cv2.GaussianBlur(invert, (21, 21), 0)

            invert_blur = 255 - blur

            sketch = cv2.divide(gray, invert_blur, scale=256.0)
            cv2.imwrite(f"static/{filename}", sketch)
            return filename
        case "blur":
            blurred = cv2.medianBlur(image, 15)

            cv2.imwrite(f"static/{filename}", blurred)
            return filename

        case "edge":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)

            edges = cv2.Canny(blur, 100, 200)

            cv2.imwrite(f"static/{filename}", edges)
            return filename

        case "face":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 3)

            cv2.imwrite(f"static/{filename}", image)
            return filename

        case "background":
            mask = np.zeros(image.shape[:2], np.uint8)

            bgModel = np.zeros((1, 65), np.float64)
            fgModel = np.zeros((1, 65), np.float64)

            rect = (20, 20, image.shape[1]-40, image.shape[0]-40)

            cv2.grabCut(image, mask, rect, bgModel, fgModel, 5, cv2.GC_INIT_WITH_RECT)
            mask = np.where((mask==2) | (mask==0), 0, 1).astype("uint8")
            result = image * mask[:, :, np.newaxis]

            cv2.imwrite(f"static/{filename}", result)
            return filename

        case "sharpen":
            kernel = np.array([
                [-1, -1, -1],
                [-1, 9, -1],
                [-1, -1, -1]
            ])

            sharpened = cv2.filter2D(image, -1, kernel)

            cv2.imwrite(f"static/{filename}", sharpened)
            return filename
    pass
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contactus")
def contactus():
    return render_template("contactus.html")

@app.route("/edit", methods=["GET","POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")

        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return "Error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imageProcessing(filename, operation)
            flash(f"Your Processed image is <a href='/static/{filename}' target='_blank'><u>here</u></a>")
            return render_template("index.html")
    return render_template("index.html")

@app.route("/background", methods=["GET","POST"])
def background():
    if request.method == "POST":
        operation = "background"

        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return "Error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imageProcessing(filename, operation)
            flash(f"Your Processed image is <a href='/static/{filename}' target='_blank'><u>here</u></a>")
            return render_template("background.html")
    return render_template("background.html")

@app.route("/sketch", methods=["GET","POST"])
def sketch():
    if request.method == "POST":
        operation = "sketch"

        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return "Error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imageProcessing(filename, operation)
            flash(f"Your Processed image is <a href='/static/{filename}' target='_blank'><u>here</u></a>")
            return render_template("sketch.html")
    return render_template("sketch.html")

@app.route("/face", methods=["GET","POST"])
def face():
    if request.method == "POST":
        operation = "face"

        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return "Error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imageProcessing(filename, operation)
            flash(f"Your Processed image is <a href='/static/{filename}' target='_blank'><u>here</u></a>")
            return render_template("face.html")
    return render_template("face.html")

@app.route("/edge", methods=["GET","POST"])
def edge():
    if request.method == "POST":
        operation = "edge"

        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return "Error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imageProcessing(filename, operation)
            flash(f"Your Processed image is <a href='/static/{filename}' target='_blank'><u>here</u></a>")
            return render_template("edge.html")
    return render_template("edge.html")

@app.route("/blur", methods=["GET","POST"])
def blur():
    if request.method == "POST":
        operation = "blur"

        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return "Error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imageProcessing(filename, operation)
            flash(f"Your Processed image is <a href='/static/{filename}' target='_blank'><u>here</u></a>")
            return render_template("blur.html")
    return render_template("blur.html")

@app.route("/gray", methods=["GET","POST"])
def gray():
    if request.method == "POST":
        operation = "gray"

        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return "Error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imageProcessing(filename, operation)
            flash(f"Your Processed image is <a href='/static/{filename}' target='_blank'><u>here</u></a>")
            return render_template("gray.html")
    return render_template("gray.html")

app.run(debug=True, port=5001)