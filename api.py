#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
from logging import Formatter, FileHandler
import tensorflow as tf
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

# Keras/TensorFlow imports
from keras.models import load_model
from tensorflow.keras.optimizers import Adamax
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
from PIL import Image as im

#----------------------------------------------------------------------------#
# App Config
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

# Enable CORS for all routes
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Upload configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGE_UPLOADS'] = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Model configuration
MODEL_PATH = os.path.join(BASE_DIR, 'SkinCancerClassificationModelhdf5nc.h5')
IMG_WIDTH = 28
IMG_HEIGHT = 28

# Cancer classifications
CANCER_CLASSES = {
    0: 'Actinic keratoses and intraepithelial carcinomae',
    1: 'Basal Cell Carcinoma',
    2: 'Benign Keratosis',
    3: 'Dermatofibroma',
    4: 'Melanocytic nevus',
    5: 'Vascular Lesion',
    6: 'Melanoma',
    7: 'No Cancer Detected'
}

# Additional info for each class
CANCER_INFO = {
    0: {
        'severity': 'moderate',
        'description': 'Pre-cancerous skin condition that may develop into squamous cell carcinoma.',
        'recommendation': 'Consult a dermatologist for evaluation and treatment.'
    },
    1: {
        'severity': 'high',
        'description': 'The most common form of skin cancer, grows slowly and rarely spreads.',
        'recommendation': 'Immediate medical consultation required for proper treatment.'
    },
    2: {
        'severity': 'low',
        'description': 'Non-cancerous growth, usually harmless but should be monitored.',
        'recommendation': 'Regular monitoring recommended. Consult dermatologist if changes occur.'
    },
    3: {
        'severity': 'low',
        'description': 'Benign fibrous nodule, generally harmless.',
        'recommendation': 'Usually no treatment needed unless causing discomfort.'
    },
    4: {
        'severity': 'low',
        'description': 'Common mole, typically benign but should be monitored.',
        'recommendation': 'Monitor for changes using ABCDE method. Annual checkup recommended.'
    },
    5: {
        'severity': 'low',
        'description': 'Abnormality of blood vessels, usually benign.',
        'recommendation': 'Consult dermatologist if rapidly changing or bleeding.'
    },
    6: {
        'severity': 'critical',
        'description': 'Most dangerous form of skin cancer. Early detection is crucial.',
        'recommendation': 'URGENT: Immediate consultation with dermatologist required.'
    },
    7: {
        'severity': 'none',
        'description': 'No signs of cancer detected in the analysis.',
        'recommendation': 'Continue regular self-examinations and annual dermatologist visits.'
    }
}

# Ensure upload directory exists
upload_dir = app.config['IMAGE_UPLOADS']
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

# Generate secret key
random_string = os.urandom(12).hex()
app.secret_key = random_string

# Load model once at startup
model = None

def load_ml_model():
    """Load the TensorFlow model"""
    global model
    try:
        model = load_model(MODEL_PATH, compile=False)
        model.compile(
            Adamax(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        app.logger.info('Model loaded successfully')
        return True
    except Exception as e:
        app.logger.error(f'Failed to load model: {str(e)}')
        return False

#----------------------------------------------------------------------------#
# Helper Functions
#----------------------------------------------------------------------------#

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(original_filename):
    """Generate unique filename to prevent collisions"""
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{timestamp}_{unique_id}.{ext}"

def analyze_image(image_path):
    """
    Analyze the uploaded image using the ML model
    Returns: dict with prediction results
    """
    try:
        # Load and preprocess image
        img = load_img(image_path, target_size=(IMG_WIDTH, IMG_HEIGHT))
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])

        # Make prediction
        predictions = model.predict(images, batch_size=10, verbose=0)
        diagnosis_class = int(np.argmax(predictions))
        confidence = float(np.max(predictions))

        # Get all class probabilities
        probabilities = {}
        for idx, prob in enumerate(predictions[0]):
            probabilities[CANCER_CLASSES[idx]] = float(prob)

        return {
            'success': True,
            'diagnosis_class': diagnosis_class,
            'diagnosis': CANCER_CLASSES.get(diagnosis_class, 'Unknown'),
            'confidence': confidence,
            'severity': CANCER_INFO[diagnosis_class]['severity'],
            'description': CANCER_INFO[diagnosis_class]['description'],
            'recommendation': CANCER_INFO[diagnosis_class]['recommendation'],
            'probabilities': probabilities
        }
    except Exception as e:
        app.logger.error(f'Analysis error: {str(e)}')
        return {
            'success': False,
            'error': f'Image analysis failed: {str(e)}'
        }

#----------------------------------------------------------------------------#
# API Routes
#----------------------------------------------------------------------------#

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Analyze uploaded skin lesion image
    Expects: multipart/form-data with 'file' field
    Returns: JSON with analysis results
    """
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please contact administrator.'
            }), 503

        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided. Please upload an image.'
            }), 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected.'
            }), 400

        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Allowed types: PNG, JPG, JPEG, GIF'
            }), 400

        # Save file with unique name
        original_filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(original_filename)
        filepath = os.path.join(app.config['IMAGE_UPLOADS'], unique_filename)
        
        file.save(filepath)
        app.logger.info(f'File saved: {unique_filename}')

        # Analyze image
        result = analyze_image(filepath)

        if result['success']:
            # Add image info to response
            result['image'] = {
                'filename': unique_filename,
                'original_filename': original_filename,
                'url': f'/api/images/{unique_filename}',
                'upload_time': datetime.now().isoformat()
            }
            return jsonify(result), 200
        else:
            # Clean up file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify(result), 500

    except Exception as e:
        app.logger.error(f'Analyze endpoint error: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/images/<filename>', methods=['GET'])
def get_image(filename):
    """Serve uploaded images"""
    try:
        return send_from_directory(app.config['IMAGE_UPLOADS'], filename)
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'error': 'Image not found'
        }), 404

@app.route('/api/info', methods=['GET'])
def get_info():
    """Get information about cancer classifications"""
    return jsonify({
        'success': True,
        'classifications': [
            {
                'id': idx,
                'name': name,
                'severity': CANCER_INFO[idx]['severity'],
                'description': CANCER_INFO[idx]['description'],
                'recommendation': CANCER_INFO[idx]['recommendation']
            }
            for idx, name in CANCER_CLASSES.items()
        ]
    }), 200

#----------------------------------------------------------------------------#
# Error Handlers
#----------------------------------------------------------------------------#

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 10MB'
    }), 413

#----------------------------------------------------------------------------#
# Logging Setup
#----------------------------------------------------------------------------#

if not app.debug:
    file_handler = FileHandler('api_error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('API started')

#----------------------------------------------------------------------------#
# Launch
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    # Load model before starting server
    print("Loading ML model...")
    if load_ml_model():
        print("✓ Model loaded successfully")
    else:
        print("✗ Failed to load model. API will return 503 errors.")
    
    port = int(os.environ.get('PORT', 2500))
    print(f"\n🚀 API Server starting on http://0.0.0.0:{port}")
    print(f"📊 Health check: http://localhost:{port}/api/health")
    print(f"📤 Analyze endpoint: http://localhost:{port}/api/analyze")
    print(f"ℹ️  Info endpoint: http://localhost:{port}/api/info\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
