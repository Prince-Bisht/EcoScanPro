from services.prediction_service import predict
def test_regression_positive():
    result=predict({'year':2027,'state':'Uttarakhand','city':'Dehradun','population':1150000,'urbanization_percentage':76})
    assert result['predicted_kg_day']>0
