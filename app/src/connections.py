from google.cloud.sql.connector import Connector
from google.cloud import Storage
from google.cloud import secretmanager
from sqlalchemy import create_engine

class Database:
    
    def __init__(self, name):
        self.connector = Connector()
        self.db_name = name
        self.pw = self._get_password("engaged-arcanum-412912","cloudsql_pwd","1")    
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
        pool = create_engine(
            "postgresql+pg8000://",
            creator=self._get_conn)
        return pool
    


class Storage():
    
    
    def __init__(self):
        self.global_bucket_name = self._get_bucket_name()
        
    
    
    def _get_bucket_name(self, project_id, secret_id, version_id):
        path = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        
        
    
    def _create_bucket(self, bucket_name, storage_class="STANDARD", location="us-west1"):
        pass
    
    def upload_file(bucket_name:str, source_name, destination):
        pass
    
    def delete_file():
        pass