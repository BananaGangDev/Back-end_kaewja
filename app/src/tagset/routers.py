from fastapi import APIRouter

router = APIRouter(
    tags=["Tagset"]
)

@router.get('/tagset')
def tagset_page():
    return {'data': 'Tagset page'}