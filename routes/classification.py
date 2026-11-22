from pathlib import Path
from flask import Blueprint,request,jsonify
from services.image_processing import prepare
bp=Blueprint('classification',__name__)
ROOT=Path(__file__).resolve().parents[1]
CATEGORIES=['Cardboard','Glass','Metal','Organic Waste','Paper','Plastic','General Waste']
GUIDANCE={
 'Plastic':'Check recycling code and local rules; clean accepted packaging.',
 'Paper':'Keep paper clean and dry; use paper recycling where accepted.',
 'Glass':'Separate carefully; follow local glass collection guidelines.',
 'Metal':'Clean accepted metal containers before recycling.',
 'Organic Waste':'Compost suitable food and garden waste where permitted.',
 'Cardboard':'Flatten and keep dry for paper/cardboard recycling.',
 'General Waste':'Use designated residual-waste collection; separate hazardous items.'}
@bp.post('/api/classify-waste')
def classify():
    f=request.files.get('image')
    if not f: return jsonify(error='Upload an image in the image field'),400
    if not f.filename.lower().endswith(('.jpg','.jpeg','.png','.webp')): return jsonify(error='Unsupported image extension'),400
    try: arr=prepare(f.read(8*1024*1024+1))
    except ValueError as e: return jsonify(error=str(e)),400
    path=ROOT/'models'/'waste_classifier.keras'
    if not path.exists(): return jsonify(error='Trained classifier not installed. This is demonstration mode; run the classifier training script with a licensed image dataset.',mode='demo',model_ready=False),503
    try:
        import tensorflow as tf
        import numpy as np
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
        model=tf.keras.models.load_model(path)
        probs=model.predict(preprocess_input(arr[None,...].copy()),verbose=0)[0]
        indices=np.argsort(probs)[::-1][:3]
        top=[{'category':CATEGORIES[int(i)],'confidence':round(float(probs[i])*100,2)} for i in indices]
        if float(probs[indices[0]])<.55: return jsonify(category=None,confidence=top[0]['confidence'],top_predictions=top,uncertain=True,message='Unable to classify this item reliably. Please upload a clearer image.')
        cat=top[0]['category']
        return jsonify(category=cat,confidence=top[0]['confidence'],top_predictions=top,uncertain=False,recommendation=GUIDANCE[cat],recycling_information='Local recycling rules vary. Confirm with your municipality.',environmental_impact='Segregation can reduce contamination and support material recovery.',mode='trained-model')
    except Exception: return jsonify(error='Classifier model could not be loaded or evaluated'),503
