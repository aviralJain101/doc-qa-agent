# main.py
from fastapi import FastAPI
from app.api.query import router as query_router
from app.api.upload import router as upload_router
from app.api.auth import router as auth_router
from app.db.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
# Include the routers
app.include_router(auth_router, prefix="/auth")
app.include_router(query_router, prefix="/api")
app.include_router(upload_router, prefix="/api")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )