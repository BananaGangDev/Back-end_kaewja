from fastapi import APIRouter
from src import connections as conn

storage = conn.Storage()

router = APIRouter(
    tags=["File system"]
)

@router.get('/paths-docs')
def get_paths_file():
    data = storage.get_all_path_files()
    
    return {'data': data}
