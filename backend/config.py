import os
from dotenv import load_dotenv

load_dotenv()


class Config:
  CLIENT_ID = os.getenv('CLIENT_ID')
  CLIENT_SECRET = os.getenv('CLIENT_SECRET')
  NUTRITION_API_URL = os.getenv('NUTRITION_API_URL')
  CHECKPOINT_PATH = os.getenv('CHECKPOINT_PATH', './src/static_files/model.ckpt')
  WEIGHTS_PATH = os.getenv('WEIGHTS_PATH', './src/static_files/food_classifier_weights.pth')
  LABEL_PATH = os.getenv('LABEL_PATH', './src/static_files/labels.json')


class ProdConfig(Config):
  DEBUG = False


class DevConfig(Config):
  DEBUG = True


def get_config():
  return ProdConfig() if os.getenv('ENV') == 'prod' else DevConfig()
