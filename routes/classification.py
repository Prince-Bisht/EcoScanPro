from pathlib import Path
from functools import lru_cache
import logging
import json
from flask import Blueprint, request, jsonify
from services.image_processing import prepare

bp = Blueprint('classification', __name__)
ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / 'models' / 'waste_classifier.keras'
CLASSES_PATH = ROOT / 'models' / 'waste_classifier_classes.json'
GUIDANCE = {
    'Plastic': 'Check recycling code and local rules; clean accepted packaging.',
    'Paper': 'Keep paper clean and dry; use paper recycling where accepted.',
    'Glass': 'Separate carefully; follow local glass collection guidelines.',
    'Metal': 'Clean accepted metal containers before recycling.',
    'Organic Waste': 'Compost suitable food and garden waste where permitted.',
    'Cardboard': 'Flatten and keep dry for paper/cardboard recycling.',
    'General Waste': 'Use designated residual-waste collection; separate hazardous items.',
}


@lru_cache(maxsize=1)
def get_classifier():
    import tensorflow as tf
    model = tf.keras.models.load_model(MODEL_PATH)
    classes = json.loads(CLASSES_PATH.read_text())
    if model.output_shape[-1] != len(classes):
        raise ValueError('Model output count does not match class mapping')
    return model, classes


@bp.post('/api/classify-waste')
def classify():
    f = request.files.get('image')
    if not f:
        return jsonify(error='Upload an image in the image field'), 400
    if not (f.filename or '').lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        return jsonify(error='Unsupported image extension'), 400
    try:
        arr = prepare(f.read(8 * 1024 * 1024 + 1))
    except ValueError as exc:
        return jsonify(error=str(exc)), 400

    if not MODEL_PATH.exists() or not CLASSES_PATH.exists():
        return jsonify(error='Trained classifier or class mapping missing.',
                       mode='demo', model_ready=False), 503
    try:
        import numpy as np
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
        model, classes = get_classifier()
        probs = model.predict(preprocess_input(arr[None, ...].copy()), verbose=0)[0]
        indices = np.argsort(probs)[::-1][:3]
        top = [{'category': classes[int(i)], 'confidence': round(float(probs[i]) * 100, 2)}
               for i in indices]
        if float(probs[indices[0]]) < 0.55:
            return jsonify(category=None, confidence=top[0]['confidence'],
                           top_predictions=top, uncertain=True,
                           message='Unable to classify this item reliably. Please upload a clearer image.')
        category = top[0]['category']
        return jsonify(category=category, confidence=top[0]['confidence'],
                       top_predictions=top, uncertain=False,
                       recommendation=GUIDANCE[category],
                       recycling_information='Local recycling rules vary. Confirm with your municipality.',
                       environmental_impact='Segregation can reduce contamination and support material recovery.',
                       mode='trained-model')
    except Exception:
        logging.exception('Classifier inference failed')
        return jsonify(error='Classifier model could not be loaded or evaluated'), 503
