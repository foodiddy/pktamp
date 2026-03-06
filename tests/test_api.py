import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.api import api_bp
from app.replay_manager import replay_manager

@pytest.fixture
def app():
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_ping(client):
    response = client.get('/api/ping')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_interfaces(client):
    response = client.get('/api/interfaces')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_list_pcaps(client):
    response = client.get('/api/pcaps')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_start_replay(client):
    from io import BytesIO
    from werkzeug.datastructures import FileStorage
    
    # Create a minimal pcap file for testing
    pcap_data = b'\xd4\xc3\xb2\xa1\x02\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
    
    response = client.post(
        '/api/pcaps',
        data={'file': (BytesIO(pcap_data), 'test.pcap')}
    )
    assert response.status_code == 200
    
    response = client.post('/api/replay', json={
        'files': ['test.pcap'],
        'interface': 'lo',
        'speed': 0
    })
    assert response.status_code == 200
    assert 'id' in response.json
    
    replay_id = response.json['id']
    
    response = client.get(f'/api/replay/{replay_id}/status')
    assert response.status_code == 200
    
    response = client.delete(f'/api/replay/{replay_id}')
    assert response.status_code == 200
    
    replay_manager.stop_replay(replay_id)

def test_upload_and_delete(client):
    from io import BytesIO
    
    pcap_data = b'\xd4\xc3\xb2\xa1\x02\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
    
    response = client.post(
        '/api/pcaps',
        data={'file': (BytesIO(pcap_data), 'delete_test.pcap')}
    )
    assert response.status_code == 200
    
    response = client.delete('/api/pcaps/delete_test.pcap')
    assert response.status_code == 200

def test_rename_pcap(client):
    from io import BytesIO
    
    pcap_data = b'\xd4\xc3\xb2\xa1\x02\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
    
    response = client.post(
        '/api/pcaps',
        data={'file': (BytesIO(pcap_data), 'rename_test.pcap')}
    )
    assert response.status_code == 200
    
    response = client.put('/api/pcaps/rename_test.pcap', json={
        'newName': 'renamed.pcap'
    })
    assert response.status_code == 200
    assert response.json['name'] == 'renamed.pcap'
