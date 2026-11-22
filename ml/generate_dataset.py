from pathlib import Path
import numpy as np
import pandas as pd

CITIES = [
 ('Delhi','Delhi',33800000,.97,.64),('Maharashtra','Mumbai',21600000,.99,.68),
 ('Karnataka','Bengaluru',14200000,.91,.59),('Tamil Nadu','Chennai',12000000,.95,.57),
 ('West Bengal','Kolkata',15300000,.87,.55),('Telangana','Hyderabad',11100000,.92,.57),
 ('Maharashtra','Pune',7500000,.84,.54),('Uttarakhand','Dehradun',1100000,.75,.43)]

def generate(path=None):
    rng=np.random.default_rng(42)
    rows=[]
    for state,city,pop2025,urban,percap in CITIES:
        for year in range(2015,2027):
            population=round(pop2025*(1.018**(year-2025)))
            urban_pct=round(min(99.5,max(40,(urban+(year-2025)*.002)*100)),2)
            pc=round(percap*(1+.008*(year-2025)),4)
            waste=round(population*pc*(1+.0018*(urban_pct-80))*(1+rng.normal(0,.025)))
            rows.append(dict(year=year,state=state,city=city,population=population,urbanization_percentage=urban_pct,estimated_waste_per_capita_kg_day=pc,total_waste_kg_day=waste))
    path=Path(path or Path(__file__).resolve().parents[1]/'data'/'indian_waste_data.csv')
    path.parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(path,index=False)
    return path
if __name__=='__main__': print(generate())
