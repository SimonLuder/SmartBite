from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routes.routes import router
from src.services.classification_srv import ClassificationModel
from fastapi.middleware.cors import CORSMiddleware
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
  """Ensures that resourceare properly initialized and cleaned up.

  Args:
      app (FastAPI): The FastAPI application instance.
  """

  try:
    # init the model
    ClassificationModel.get_instance()
    print('Model initialized successfully')

    yield  # yield = wait for the app to finish
  except Exception as e:
    print(f'Error during initialization: {e}')
    raise e


app = FastAPI(lifespan=lifespan)

# enable CORS for all routes in dev mode
if os.getenv('ENV') != 'prod':
  app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )


# the application routes
app.include_router(router)
