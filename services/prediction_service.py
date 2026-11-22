from pathlib import Path
import joblib
import pandas as pd
from ml.train_regression import FEATURES
ROOT=Path(__file__).resolve().parents[1]
_model=None

def model():
    global _model
    if _model is None:
        path=ROOT/'models'/'waste_regression.joblib'
        if not path.exists(): raise RuntimeError('Regression model unavailable. Run python ml/train_regression.py')
        _model=joblib.load(path)
    return _model

def dataset(): return pd.read_csv(ROOT/'data'/'indian_waste_data.csv')

def predict(record):
    required=['year','state','city','population','urbanization_percentage']
    if any(k not in record for k in required): raise ValueError('Missing required prediction fields')
    year=int(record['year']); population=int(record['population']); urban=float(record['urbanization_percentage'])
    if not 2010<=year<=2050 or population<=0 or not 0<=urban<=100: raise ValueError('Year, population or urbanization out of range')
    df=dataset()
    matched=df[(df.city==record['city']) & (df.state==record['state'])]
    if matched.empty: raise ValueError('Select a supported state and city')
    pc=float(record.get('estimated_waste_per_capita_kg_day',matched.iloc[-1].estimated_waste_per_capita_kg_day))
    if not .05<=pc<=5: raise ValueError('Per capita waste must be between 0.05 and 5 kg/day')
    row={'year':year,'state':record['state'],'city':record['city'],'population':population,'urbanization_percentage':urban,'estimated_waste_per_capita_kg_day':pc}
    value=max(0,float(model().predict(pd.DataFrame([row],columns=FEATURES))[0]))
    return {'predicted_kg_day':round(value,2),'predicted_tonnes_day':round(value/1000,2),'label':'Model estimate based on synthetic demonstration data','inputs':row}
