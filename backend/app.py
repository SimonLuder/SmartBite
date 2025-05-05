from fastapi import FastAPI
from src.routes.routes import router

# instantiate the FastAPI application
app = FastAPI()


# the application routes
app.include_router(router)
