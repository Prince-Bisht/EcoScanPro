from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT=Path(__file__).resolve().parents[1]
FEATURES=['year','state','city','population','urbanization_percentage','estimated_waste_per_capita_kg_day']
TARGET='total_waste_kg_day'

def train():
    df=pd.read_csv(ROOT/'data'/'indian_waste_data.csv').dropna()
    # Chronological holdout: earlier years train, final two years test.
    train_df=df[df.year<=2024]
    test_df=df[df.year>=2025]
    pre=ColumnTransformer([('cat',OneHotEncoder(handle_unknown='ignore'),['state','city']),('num',StandardScaler(),['year','population','urbanization_percentage','estimated_waste_per_capita_kg_day'])])
    pipe=Pipeline([('preprocess',pre),('regressor',LinearRegression())])
    pipe.fit(train_df[FEATURES],train_df[TARGET])
    predicted=pipe.predict(test_df[FEATURES])
    metrics={'mae_kg_day':float(mean_absolute_error(test_df[TARGET],predicted)),'rmse_kg_day':float(np.sqrt(mean_squared_error(test_df[TARGET],predicted))),'r2':float(r2_score(test_df[TARGET],predicted)),'train_rows':len(train_df),'test_rows':len(test_df),'test_years':[2025,2026],'dataset':'synthetic demonstration data'}
    (ROOT/'models').mkdir(exist_ok=True)
    joblib.dump(pipe,ROOT/'models'/'waste_regression.joblib')
    (ROOT/'models'/'regression_metrics.json').write_text(json.dumps(metrics,indent=2))
    return metrics
if __name__=='__main__': print(train())
