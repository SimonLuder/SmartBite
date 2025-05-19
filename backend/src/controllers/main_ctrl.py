import logging
from typing import Dict
from fastapi import HTTPException

from src.services.classification_srv import ClassificationModel
from src.services import nutrition_srv


async def classify(image_bytes: bytes) -> Dict:
  """Classify food items and fetch nutrition scores.

  Args:
      some_data (_type_): data to be classified.

  Returns:
      _type_: the classification result and nutrition scores.
  """

  try:
    # get classifications
    model = ClassificationModel.get_instance()

    label, probability = model.inference(image_bytes)

    # fetch nutrition scores based on the classification result
    scores = await nutrition_srv.get_nutrition_scores(label)
    
    return {'label': label, 'probability': round(probability, 3), 'nutrition': scores}

  except Exception as e:
    logging.exception(f'Error classifying food: {e}')
    raise HTTPException(status_code=400, detail='Error in classify function')
