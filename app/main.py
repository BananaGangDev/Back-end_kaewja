# Web
import uvicorn
from fastapi import FastAPI
from src.auth.routers import router as auth_routes
from app.src.concordancer.routers import router as concor_routes
from app.src.error_tagger.routers import router as errortag_routes
from app.src.file_system.routers import router as file_routes
from app.src.tagset.routers import router as tagset_routes



app = FastAPI()
app.include_router(auth_routes)
app.include_router(concor_routes)
app.include_router(errortag_routes)
app.include_router(file_routes)
app.include_router(tagset_routes)


# python main.py
if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)