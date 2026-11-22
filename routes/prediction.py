from flask import Blueprint,request,jsonify
from services.prediction_service import dataset,predict,model
from ml.train_regression import FEATURES
import pandas as pd
bp=Blueprint('prediction',__name__)
@bp.get('/api/dataset')
def data():
    df=dataset()
    return jsonify({'disclaimer':'Synthetic demonstration dataset — not official Indian government data.','records':df.to_dict('records'),'cities':df[['state','city']].drop_duplicates().to_dict('records')})
@bp.post('/api/predict')
def prediction():
    try: return jsonify(predict(request.get_json(silent=True) or {}))
    except (ValueError,TypeError,OverflowError) as exc: return jsonify(error=str(exc)),400
    except Exception: return jsonify(error='Prediction model unavailable'),503
@bp.get('/api/model-comparison')
def comparison():
    try:
        df=dataset(); vals=model().predict(df[FEATURES]); records=[]
        for row,p in zip(df.to_dict('records'),vals): records.append({'year':row['year'],'city':row['city'],'actual':row['total_waste_kg_day'],'predicted':round(max(0,float(p)))})
        return jsonify(records=records,disclaimer='Actual means synthetic dataset value, not measured waste.')
    except Exception: return jsonify(error='Model unavailable'),503
