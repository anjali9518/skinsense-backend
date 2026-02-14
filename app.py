#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from secrets import token_bytes
from flask import Flask, render_template, request, session, url_for, redirect
import logging
from logging import Formatter, FileHandler
import tensorflow as tf
from werkzeug.utils import secure_filename

import os
# -----------------------------------------KERAS MODEL IMPLEMENTATION----------------------------------------------------- #

from keras.models import load_model
from tensorflow.keras.optimizers import Adam, Adamax
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
import numpy as np
from PIL import Image as im

# -----------------------------------------KERAS MODEL IMPLEMENTATION----------------------------------------------------- #

import json

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

# Directory for image uploads
app.config['IMAGE_UPLOADS'] = r'C:\Anjali\mysite\static\image'

# Ensure the upload directory exists
upload_dir = app.config['IMAGE_UPLOADS']
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

# Generate a random secret key for session management
random_string = os.urandom(12).hex()
print("Secret key is: ", random_string)
app.secret_key = random_string

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
@app.route('/home')
def home():
    return render_template("forms/index.html")

@app.route('/try_now')
def try_now():
    return render_template("forms/try_now.html")

@app.route('/learn')
def learn():
    return render_template("forms/learn.html")



@app.route("/q2", methods=['GET', 'POST'])
def q2():
    if request.method == 'POST':
        uploaded_image = request.files['file']
        uploaded_image_filename = uploaded_image.filename
        # Save the uploaded image
        uploaded_image.save(os.path.join(app.config['IMAGE_UPLOADS'], uploaded_image_filename))
        local_filename = os.path.join(app.config['IMAGE_UPLOADS'], uploaded_image_filename)
        local_filename2 = uploaded_image_filename  # Store just the filename for display

        # Load the image for processing
        image4 = im.open(local_filename)
        image4.save(local_filename)

        model_path = r'C:\Anjali\mysite\SkinCancerClassificationModelhdf5nc.h5'

        # Dimensions of the images
        img_width, img_height = 28, 28

        # Load the model
        model = load_model(model_path, compile=False)
        model.compile(Adamax(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

        # Load the image
        img = load_img(local_filename, target_size=(img_width, img_height))
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])

        # Predict image
        predictions = model.predict(images, batch_size=10)
        diagnosis_class = np.argmax(predictions)

        cancer_classes = {
            0: 'Actinic keratoses and intraepithelial carcinomae',
            1: 'Basal Cell Carcinoma',
            2: 'Benign Keratosis',
            3: 'Dermatofibroma',
            4: 'melanocytic nevus', 
            5: 'Vascular Lesion',
            6: 'Melanoma',
            7: 'No Cancer Detected'
        }
        
        # Get the predicted cancer type
        predicted_cancer = cancer_classes.get(diagnosis_class, 'Unknown')

        return render_template("forms/q2_new.html", filename=local_filename2, diagnosis=predicted_cancer)

    elif request.method == 'GET':
        return render_template("forms/q2_new.html")

@app.route('/q2/<filename>')
def displayQ2(filename):
    return redirect(url_for('static', filename='image/' + filename), code=301)


# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 2500))
    app.run(host='0.0.0.0', port=port)
