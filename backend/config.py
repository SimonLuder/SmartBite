import os
from dotenv import load_dotenv

load_dotenv()


class Config:
  # to do: add more config variables
  SOME_KEY = os.getenv('SOME_KEY')


class ProdConfig(Config):
  DEBUG = False


class DevConfig(Config):
  DEBUG = True


def get_config():
  return ProdConfig() if os.getenv('ENV') == 'prod' else DevConfig()
