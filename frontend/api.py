import requests
import os

from dotenv import load_dotenv

load_dotenv()

# change this to actual backend URL
BACKEND_URL = os.getenv('BACKEND_URL', 'http://127.0.0.1:8000')


# status check function
def check_status():
  try:
    response = requests.get(f'{BACKEND_URL}/api/status')
    response.raise_for_status()
    print(response.json())
    return None
  except requests.exceptions.RequestException as e:
    print(f'Error checking status: {e}')
    return None


### image Analysis Function ###
def analyze_image(image_file):
  try:
    files = {'image': image_file}
    response = requests.post(f'{BACKEND_URL}/api/classify', files=files)
    response.raise_for_status()
    return response.json()
  except requests.exceptions.RequestException as e:
    print(f'Error analyzing image: {e}')
    return {
      'label': 'Error',
      'confidence': 0.0,
      'nutrition': {},
      'error': str(e),
    }
