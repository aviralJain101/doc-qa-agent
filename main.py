# main.py
from fastapi import FastAPI
from app.api.query import router as query_router
from app.api.upload import router as upload_router

app = FastAPI()

# Include the routers
app.include_router(query_router)
app.include_router(upload_router)