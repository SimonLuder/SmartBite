import re
import httpx
from typing import Dict
from oauthlib.oauth1 import Client
from urllib.parse import urlencode

import config


CONFIG = config.get_config()

# initialize the OAuth1 client
# signature_type = 'QUERY' ensures that the signature is
# included in the url query parameters
signer = Client(client_key=CONFIG.CLIENT_ID, client_secret=CONFIG.CLIENT_SECRET, signature_type='QUERY')


async def get_nutrition_scores(classification_result: str) -> Dict:
  """Get nutrition scores based on the classification result.

  Args:
      classification_result (str): the classification result from the food classification service.

  Returns:
      Dict: the nutrition scores for the classified food item.
  """

  # the request parameters for the nutrition API
  # search_expression is the food item to be classified
  # format is the response format we want from the API
  params = {'search_expression': classification_result, 'format': 'json'}
  url_with_params = CONFIG.NUTRITION_API_URL + '?' + urlencode(params)

  # sign the url with the OAuth1 client
  signed_url, _, _ = signer.sign(url_with_params, http_method='GET')

  # make the request
  async with httpx.AsyncClient() as client:
    res = await client.get(signed_url)

  if res.status_code != 200:
    raise Exception(f'API call failed: {res.status_code} - {res.text}')

  data = res.json()

  # fatsecret api does only return 200 status code
  # therefore check if the response data contains an error
  if data.get('error'):
    raise Exception(f'API call failed: {data.get("error")}')

  # get the first food item from the response
  stats = data.get('foods').get('food')[0]

  # the pattern (regex) to extract the nutrition values
  pattern = r'Calories:\s*([\d.]+kcal)\s*\|\s*Fat:\s*([\d.]+g)\s*\|\s*Carbs:\s*([\d.]+g)\s*\|\s*Protein:\s*([\d.]+g)'
  match = re.search(pattern, stats.get('food_description'))

  if match:
    calories = match.group(1)
    fat = match.group(2)
    carbs = match.group(3)
    protein = match.group(4)
  else:
    # if the regex fails, set all values to NaN
    calories, fat, carbs, protein = 'NaN'

  return {
    'serving_size': 'Per 100g',
    'calories': calories,
    'protein': protein,
    'carbohydrates': carbs,
    'fat': fat,
    'food_url': stats.get('food_url'),
  }
