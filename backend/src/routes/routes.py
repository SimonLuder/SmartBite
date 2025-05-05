from fastapi import APIRouter

from src.controllers import main_ctrl

# instantiate the router
router = APIRouter()


# general routes
@router.get('/')
async def root():
  return {'msg': 'Welcome to the SmartBite backend!'}


@router.get('/api/status')
async def status():
  return {'msg': 'ok!'}


# classification routes
@router.post('/api/classify')
async def classify():
  return await main_ctrl.classify()
