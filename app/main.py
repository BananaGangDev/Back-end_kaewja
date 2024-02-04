# Web
import uvicorn
from fastapi import FastAPI
from src.auth.router import router as auth_routes
from src.concordancer.router import router as concor_routes
from src.error_tagger.router import router as errortag_routes
from src.file_system.router import router as file_routes
from src.tagset.router import router as tagset_routes



app = FastAPI()
app.include_router(auth_routes)
app.include_router(concor_routes)
app.include_router(errortag_routes)
app.include_router(file_routes)
app.include_router(tagset_routes)


# python main.py
if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)