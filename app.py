from flask import Flask, render_template, request, redirect, url_for
import os
import random

app = Flask(__name__, static_url_path='/static')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return redirect(url_for('index'))

@app.route('/wardrobe')
def wardrobe():
    wardrobe_images = get_uploaded_images()
    return render_template('wardrobe.html', wardrobe_images=wardrobe_images)

@app.route('/shuffle')
def shuffle():
    wardrobe_images = get_uploaded_images()

    if len(wardrobe_images['tops']) < 2 or len(wardrobe_images['bottoms']) < 2:
        return render_template('shuffle.html', error_message="Not enough items to shuffle.")

    shuffled_outfit = {
        'top': random.choice(wardrobe_images['tops']),
        'bottom': random.choice(wardrobe_images['bottoms'])
    }

    return render_template('shuffle.html', shuffled_outfit=shuffled_outfit)

def get_uploaded_images():
    tops_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'tops')
    bottoms_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'bottoms')

    tops = [f for f in os.listdir(tops_folder) if os.path.isfile(os.path.join(tops_folder, f))]
    bottoms = [f for f in os.listdir(bottoms_folder) if os.path.isfile(os.path.join(bottoms_folder, f))]

    wardrobe_images = {'tops': tops, 'bottoms': bottoms}
    return wardrobe_images

if __name__ == '__main__':
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'tops'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'bottoms'), exist_ok=True)
    app.run(debug=True)
