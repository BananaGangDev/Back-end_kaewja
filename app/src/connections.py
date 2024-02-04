from google.cloud.sql.connector import Connector
from google.cloud import secretmanager
import pg8000
import sqlalchemy

class Database:
    
    def __init__(self, name):
        self.connector = Connector()
        self.db_name = name
        self.pw = self.get_password("engaged-arcanum-412912","cloudsql_pwd","1")    
    def _get_conn(self):
        
        conn = self.connector.connect(
            "engaged-arcanum-412912:us-west1:kaewja-instance",
            "pg8000",
            user="postgres",
            password=self.pw,
            db=self.db_name
        )
        return conn
    def _get_password(self,project_id, secret_id, version_id):
        
        client = secretmanager.SecretManagerServiceClient()
        
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        
        response = client.access_secret_version(request={'name':name})
        password = response.payload.data.decode("UTF-8")
        return password
    def get_db(self):
        pool= sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=self.get_conn)
        return pool
    


class Storage():
    
    
    def __init__():
        pass
    
    def get_storage():
        pass
    
    def close_storage():
        pass
        