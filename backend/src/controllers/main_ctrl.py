import logging
from fastapi import HTTPException

from src.services import classification_srv, nutrition_srv


async def classify(some_data):
  """Classify food items and fetch nutrition scores.

  Args:
      some_data (_type_): data to be classified.

  Returns:
      _type_: the classification result and nutrition scores.
  """

  try:
    # get classifications
    result = await classification_srv.classify_food(some_data)
    # fetch nutrition scores based on the classification result
    scores = await nutrition_srv.get_nutrition_scores(result)
    return {'result': result, 'scores': scores}

  except Exception as e:
    logging.exception(f'Error classifying food: {e}')
    raise HTTPException(status_code=400, detail='Error in classify function')
