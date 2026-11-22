import pytest
from app import create_app
@pytest.fixture
def client():
    app=create_app();app.config['TESTING']=True
    return app.test_client()
def test_health(client): assert client.get('/api/health').status_code==200
def test_pages(client):
    for url in ['/','/prediction','/scanner','/chatbot','/about']: assert client.get(url).status_code==200
def test_dataset(client): assert len(client.get('/api/dataset').json['records'])>=80
def test_prediction(client):
    res=client.post('/api/predict',json={'year':2027,'state':'Delhi','city':'Delhi','population':35000000,'urbanization_percentage':97})
    assert res.status_code==200 and res.json['predicted_kg_day']>0
def test_bad_prediction(client): assert client.post('/api/predict',json={'year':3000}).status_code==400
def test_chat_empty(client): assert client.post('/api/chat',json={'message':''}).status_code==400
def test_chat_fallback(client): assert client.post('/api/chat',json={'message':'What is composting?'}).json['response']
def test_missing_image(client): assert client.post('/api/classify-waste').status_code==400
def test_bad_image(client):
    from io import BytesIO
    res=client.post('/api/classify-waste',data={'image':(BytesIO(b'bad data'),'x.png')})
    assert res.status_code==400
