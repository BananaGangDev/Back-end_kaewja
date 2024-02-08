# Web
import uvicorn
from fastapi import FastAPI

# routes
from src.auth.routers import router as auth_routes
from src.concordancer.routers import router as concor_routes
from src.error_tagger.routers import router as errortag_routes
from src.file_system.routers import router as file_routes
from src.tagset.routers import router as tagset_routes

# Data
from src.connections import global_db

global_db.get_base().metadata.create_all(bind=global_db.get_engine())

app = FastAPI()
app.include_router(auth_routes)
app.include_router(concor_routes)
app.include_router(errortag_routes)
app.include_router(file_routes)
app.include_router(tagset_routes)



# python main.py
if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)