import pytest
from rest_framework.test import APIClient
from rest_framework.viewsets import ModelViewSet
from app.models import StockReading, StockReadingHistory

from mock import MagicMock
@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def stockreading():
    stock_reading = StockReading()
    stock_reading.id = 1
    stock_reading.ref_id = 1234567890123
    stock_reading.expiration_date = "2019-12-12T00:00"
    return stock_reading

ref_id = 1234567890123

@pytest.mark.django_db
def test_view_status_code(client):
    resp = client.get('/app/stockreading/')
    assert resp.status_code == 200

@pytest.mark.django_db
def test_view_create(client):
    resp = client.post('/app/stockreading/', data={"ref_id":ref_id, "expiration_date":"2019-12-12T00:00"})
    assert resp.status_code == 201


@pytest.mark.django_db
def test_view_update(client, monkeypatch, stockreading):
    monkeypatch.setattr(ModelViewSet, 'update', MagicMock(return_value=True))
    monkeypatch.setattr(StockReading, 'get_from_id', MagicMock(return_value=stockreading))
    monkeypatch.setattr(StockReadingHistory, 'save', MagicMock(return_value=True))

    resp = client.put('/app/stockreading/1/', data={"ref_id":ref_id, "expiration_date":"2019-12-12T00:00"})
    assert resp.status_code == 200

