import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('__file__'), '..')))
from fastapi.testclient import TestClient
from api.main import app

def run_test():
    client = TestClient(app)
    payload = {
        'species': 'canine',
        'priorAntibiotics': True,
        'notes': 'Patient presents with lethargy and lack of appetite.',
        'hardwareTier': 'advanced',
        'allergies': 'none',
        'renalFunction': 'normal'
    }
    print('Sending POST request to /api/upload...')
    response = client.post('/api/upload', json=payload)
    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        print('Response OK')
    else:
        print(response.text)
        
if __name__ == '__main__':
    run_test()
