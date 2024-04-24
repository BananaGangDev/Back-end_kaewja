from google.cloud.sql.connector import Connector
from google.cloud import storage
from google.cloud import secretmanager
from fastapi import UploadFile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from io import StringIO


class Database: 
    def __init__(self):
        # user
        self.connector = Connector()
        self.client = secretmanager.SecretManagerServiceClient()
        
        self.path = "projects/{id}/secrets/{secret}/versions/{ver}"
        
        self.db_name = self._get_secret("engaged-arcanum-412912","active_db","1")
        self.pw = self._get_secret("engaged-arcanum-412912","cloudsql_pwd","1")
        self.instance = self._get_secret("engaged-arcanum-412912", "instance", "1")
        
        self.engine = create_engine(
            "postgresql+pg8000://",
            creator=self._get_conn, connect_args={'check_same_thread':False})
        
        self.base = declarative_base()    
    def _get_conn(self):
        conn = self.connector.connect(
            "engaged-arcanum-412912:"+self.instance,
            "pg8000",
            user="postgres",
            password=self.pw,
            db=self.db_name
        )
        return conn 
    def _get_secret(self,project_id, secret_id, version_id):
        try:
            response = self.client.access_secret_version(request={'name':self.path.format(id=project_id,secret=secret_id,ver=version_id)})
            data = response.payload.data.decode("UTF-8")
        except Exception as error:
            print(error)
            
        return data
    
    # // Generally use
    def get_sessionlocal(self):
        session_local = sessionmaker(bind=self.engine, autocommit=False, autoflush = True)
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
        self.global_corpus = self.storage_client.bucket(self._get_bucket_name("engaged-arcanum-412912","corpus_storage_name","1"))
        
    def _get_bucket_name(self, project_id, secret_id, version_id):
        
        client = secretmanager.SecretManagerServiceClient()
        path = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        
        response = client.access_secret_version(request={'name':path})
        password = response.payload.data.decode("UTF-8")
        return password
    
    def get_all_path_files(self, in_corpus:bool=False):
        try:
            if not in_corpus:    
                files = self.storage_client.list_blobs(self.global_bucket)
                result = [file.name for file in files]
                
            else:
                files = self.storage_client.list_blobs(self.global_corpus)
                result = [file.name for file in files]
            return True, result
        except Exception as error:
            print(f"Path file\nAn error occurred: {error}")
            return False, error
                
    def create_folder(self,  folder_name:str):
        try:
            #// Create both bucket automatically
            blob_corpus = self.global_corpus.blob(f"{folder_name}/")
            blob_bucket = self.global_bucket.blob(f"{folder_name}/")
            
            blob_corpus.upload_from_string('')
            blob_bucket.upload_from_string('')
            return True, "_"
        except Exception as error:
            print(f"Create Folder\nAn error occurred: {error}")
            return False, error
    
    def delete_folder(self, folder_name:str):
        try:
            blob_cor = list(self.global_corpus.list_blobs(prefix=folder_name))
            blob_buc = list(self.global_bucket.list_blobs(prefix=folder_name))
            
            for blob in blob_cor:
                blob.delete()
            for blob in blob_buc:
                blob.delete()   
                
            return True, "_"
        except Exception as error:
            print(f"Delete folder\nAn error occurred: {error}")
            return False, error
    
    def delete_blob(self, blob_name:str, in_corpus:bool=False):
        try:
            blob_buc = self.global_bucket.blob(blob_name)
            if in_corpus:
                blob_cor = self.global_corpus.blob(f"{blob_name[:len(blob_name)-4]}.txt") #// .txt file
                blob_cor.delete()

            blob_buc.delete()
            return True, "_"
        except Exception as error:
            print(f"Delete blob\nAn error occurred: {error}")  
            return False, error 
        
    def rename_folder(self, old_name:str, new_name:str):
        try:
            blobs_buc = self.global_bucket.list_blobs(prefix=old_name)
            for blob in blobs_buc:
                
                new_blob_name = blob.name.replace(old_name, new_name)
                new_blob_buc = self.global_bucket.blob(new_blob_name)
                new_blob_buc.upload_from_string(blob.download_as_bytes(), content_type=blob.content_type)
                blob.delete()
                
            blobs_cor = self.global_corpus.list_blobs(prefix=old_name)
            for blob in blobs_cor:
                
                new_blob_name = blob.name.replace(old_name, new_name)
                new_blob_cor = self.global_corpus.blob(new_blob_name)
                new_blob_cor.upload_from_string(blob.download_as_bytes(), content_type=blob.content_type)
                #// Delete the file in old folder
                blob.delete()

            
            return True, "_"
        except Exception as error:
            print(f"Rename folder\nAn error occurred: {error}")
            return False, error
    
    def rename_blob(self, old_name:str, new_name:str, in_corpus:bool):
        try:
            blob_buc = self.global_bucket.blob(old_name)
            new_blob_buc = self.global_bucket.rename_blob(blob_buc, new_name)
            
            if in_corpus:
                name_cor = old_name[:len(old_name)-4] + ".txt"
                new_name_cor = new_name[:len(new_name)-4] + ".txt"
                blob_cor = self.global_corpus.blob(name_cor)
                new_blob_cor = self.global_corpus.rename_blob(blob_cor, new_name_cor)
            
            return True, "_"
        except Exception as error:
            print(f"Rename blob\n An error occurred: {error}")
            return False, error
    
    def upload_file(self, file:UploadFile):
        try:
            blob = self.global_bucket.blob(file.filename)
            blob.upload_from_file(file.file)
            return True
        except Exception as e:
            print(str(e))
            print("Connection file\nFunction: upload file")
            return False

    def upload_file_corpus(self, file:UploadFile):
        try:
            blob_corpus = self.global_corpus.blob(file.filename)
            blob_corpus.upload_from_file(file.file)
            return True
        except Exception as e:
            print(str(e))
            print("Connection file\nFunction: upload_file_corpus")
            return False
    
    def download_file(file_name:str):
        pass
    
    def extract_into_txt(self,file_name:str):
        #// Get it as txt file
        blob_buc = self.global_bucket.blob(file_name)
        downloaded_blob = blob_buc.download_as_text().decode("utf-8")
        
        
        if file_name.count("/") != 0:
            splitted_file_name = file_name.split("/")
            name = splitted_file_name[-1]
            
        elif file_name.count("/") == 0:
            name = file_name
        
        #// Get folder name
        folders = "/".join(splitted_file_name[:2])
        
        blob_cor = self.global_corpus.blob(f"{file_name[:len(file_name)-4]}.txt")
        blob_cor.upload_from_string(downloaded_blob)    
      
        

global_db = Database()
global_st= Storage() 