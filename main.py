import os
from flask import Flask, flash, request, render_template, redirect, url_for, Markup
from werkzeug.utils import secure_filename
import cv2

UPLOAD_FOLDER = './static/user_uploads/'
CONVERTED_UPLOADS = "./static/converted_uploads/"
ALLOWED_EXTENSIONS = {'webp', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "fwj#ok12"

def convert_file(file,opertation):
    img = cv2.imread(f"./static/user_uploads/{file}")
    filename = file.split('.')
    match opertation:
        case "png":
            img = cv2.imwrite(f"./static/converted_uploads/{filename[0]}.png",img)
            return ".png"
        case "jpeg":
            img = cv2.imwrite(f"./static/converted_uploads/{filename[0]}.jpeg",img)
            return ".jpeg"
        case "gs":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.imwrite(f"./static/converted_uploads/{filename[0]}.png",img)
            return ".png"
        case "webp":
            img = cv2.imwrite(f"./static/converted_uploads/{filename[0]}.webp",img)
            return ".webp"


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/about')
def about():
    flash("About Page is Under Development :D")
    return render_template('index.html')

@app.route('/home')
def home():
    flash("Home Page is Under Development :D")
    return render_template('index.html')

@app.route('/login')
def login():
    flash("Login Page is Under Development :D")
    return render_template('index.html')

@app.route('/signup')
def signup():
    flash("Signup Page is Under Development :D")
    return render_template('index.html')

@app.route('/edit',methods=['GET','POST'])
def edit():
    for f in os.listdir(CONVERTED_UPLOADS):
        f = os.path.join(CONVERTED_UPLOADS,f)
        os.remove(f)
    for f in os.listdir(UPLOAD_FOLDER):
        f = os.path.join(UPLOAD_FOLDER,f)
        os.remove(f)
    if request.method == "POST":
        operation = request.form.get("file-type")
        if 'file' not in request.files:
            return "Error!"
        file = request.files['file']
        if file.filename == "":
            return render_template('index.html', error="There was no file found")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            op = convert_file(filename, operation)
            filename = filename.split('.')[0]
            flash(f'Your Image is <a href="./static/converted_uploads/{filename}{op}">Here</a>')
            return render_template("index.html", error="File Was Submitted")
        else:
            return render_template("index.html",error="Wrong File Extension Submitted")

app.run(debug=True, port=500)
