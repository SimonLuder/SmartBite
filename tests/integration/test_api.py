import requests
import pytest
import os
from pathlib import Path

API_URL = os.environ.get('API_URL', 'http://localhost:8000')


def test_api_status():
  """test that API status endpoint responds correctly"""
  response = requests.get(f'{API_URL}/api/status')
  assert response.status_code == 200
  assert response.json().get('msg') == 'ok!'


def test_classify_endpoint():
  """test that classification endpoint
  - tests the model classification functionality
  - tests the nutrition information retrieval"""

  # get a sample image from the fixtures directory
  image_path = Path(__file__).parent.parent / 'fixtures' / 'sample_images' / 'hamburger.jpg'
  assert image_path.exists(), f'Test image not found at {image_path}'

  # open the image and send it to the classify endpoint
  with open(image_path, 'rb') as img:
    files = {'image': img}
    response = requests.post(f'{API_URL}/api/classify', files=files)

  assert response.status_code == 200
  result = response.json()
  assert 'label' in result
  assert 'probability' in result
  assert 'nutrition' in result
