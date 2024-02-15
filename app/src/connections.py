from google.cloud.sql.connector import Connector
from google.cloud import storage
from google.cloud import secretmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class Database: 
    def __init__(self):
        # user
        self.connector = Connector()
        self.client = secretmanager.SecretManagerServiceClient()
        
        self.path = "projects/{id}/secrets/{secret}/versions/{ver}"
        
        self.db_name = self._get_secret("engaged-arcanum-412912","active_db","1")
        self.pw = self._get_secret("engaged-arcanum-412912","cloudsql_pwd","1")
        
        self.engine = create_engine(
            "postgresql+pg8000://",
            creator=self._get_conn, connect_args={'check_same_thread':False})
        
        self.base = declarative_base()    
    def _get_conn(self):
        conn = self.connector.connect(
            "engaged-arcanum-412912:us-west1:kaewja-instance",
            "pg8000",
            user="postgres",
            password=self.pw,
            db=self.db_name
        )
        return conn 
    def _get_secret(self,project_id, secret_id, version_id):
        response = self.client.access_secret_version(request={'name':self.path.format(id=project_id,secret=secret_id,ver=version_id)})
        data = response.payload.data.decode("UTF-8")
        return data
    
    # // Generally use
    def get_sessionlocal(self):
        session_local = sessionmaker(bind=self.engine, autocommit=False, autoflush = False)
        db = session_local()
        
        return db     
    def get_base(self):
        return self.base
    def get_engine(self):
        return self.engine
    
    

class Storage:
    
    def __init__(self):
        self.storage_client = storage.Client()
        self.global_bucket = self.storage_client.bucket(self._get_bucket_name("engaged-arcanum-412912","main_storage_name","1"))
        
        
    def _get_bucket_name(self, project_id, secret_id, version_id):
        
        client = secretmanager.SecretManagerServiceClient()
        path = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        
        response = client.access_secret_version(request={'name':path})
        password = response.payload.data.decode("UTF-8")
        return password
    def get_all_path_files(self):
        files = self.storage_client.list_blobs(self.global_bucket)
        result = [file.name for file in files]
        
        return result    
    
    # // Below this line, Not test function yet
    def upload_file(self,source_file_name, destination):
        
        blob = self.global_bucket.blob(destination)
        blob.upload_from_filename(source_file_name)
        
        return f'Upload successfully'
     
    def delete_file(self, filename):
        
        blob = self.global_bucket.blob(filename)
        blob.delete()
        
        return "Delete successfully"
    
    def download_file(self,filename, destination):

        try:
            blob = self.global_bucket.blob(filename)
            blob.download_to_file(destination)
        except Exception as e:
            return "Fail to download"
        
        return f"Successfully download"
    
    def create_folder(self):
        pass
        

global_db = Database()
    