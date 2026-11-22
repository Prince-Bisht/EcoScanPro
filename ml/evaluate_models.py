from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    path=ROOT/'models'/'regression_metrics.json'
    print(json.dumps(json.loads(path.read_text()),indent=2) if path.exists() else 'Run regression training first')
    print('Classifier evaluation requires an independent labeled test set; no test accuracy is claimed.')
