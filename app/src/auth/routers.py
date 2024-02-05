from fastapi import APIRouter
import sqlalchemy
from src import connections as conn


router = APIRouter(
    tags=["Authentication"]
)

@router.get("/")
def index():
    
    db_conn = conn.Database("db-dev")
    
    with db_conn.get_db().connect() as db:
        results = db.execute(sqlalchemy.text("SELECT NOW();")).fetchall()
        
        print(type(results))
        print(results)

    return {"data": results[0][0].strftime("%Y-%m-%d %H:%M:%S.%f %Z")}

@router.get('/login')
def login_page():
    return {"page": "Login page"}


@router.get("/changepassword")
def changepassword_page():
    pass