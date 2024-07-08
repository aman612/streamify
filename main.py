from fastapi import FastAPI

from .api.routes import base_router as Router


app = FastAPI()

app = FastAPI(title="VideoManipulator")

app.include_router(Router, prefix="/api")
