from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routes.routes import router
from src.services.classification_srv import ClassificationModel


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


# the application routes
app.include_router(router)
