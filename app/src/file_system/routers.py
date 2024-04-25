from fastapi import APIRouter, HTTPException, File, UploadFile

from src.connections import global_st
from .exceptions import (validate_folder_name, check_existing)


router = APIRouter(
    tags=["File system"],
    prefix="/sys"
)

@router.get('/paths')
async def all_uncleaned_paths(in_corpus:bool=False):
    is_successful, result = global_st.get_all_path_files(in_corpus=in_corpus)
    if not is_successful:
        raise HTTPException(status_code=503, detail=f"Service Unavailable, Google storage has a problem: {result}")
    else:
        return {'paths': result}

#TODO
@router.get("/download")
async def download_file(file_name:str, in_courpus:bool=False):
    
    result, is_successful = global_st.download_file(in_corpus=in_courpus, file_name=file_name)
    if is_successful:
        return result
    elif result == :
        

@router.post("/create-folder")
async def sys_create_folder(folder_name:str):
    
    if validate_folder_name(name=folder_name):
        is_successful, result = global_st.create_folder(folder_name=folder_name)    
        if not is_successful:
            raise HTTPException(status_code=503, detail=f"Service Unavailable, Google storage has a problem")
        else:
            return {"detail": f"Create {folder_name} successfully"}

    else:
        raise HTTPException(status_code=400, detail=f"The folder name is incorrect")
    
@router.post("/upload")
async def sys_upload_file(file:UploadFile):
    ALLOWED_TYPE = ["application/pdf", "text/plain", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]

    #// pdf, txt, docx
    if file.content_type in ALLOWED_TYPE:
        #// Storage
        is_successful = global_st.upload_file(file=file)
        if is_successful:
            return {"detail": f"Upload {file.filename} successfully"}
        else:
            raise HTTPException(status_code=500, detail=f"Service Unavailable, Storage has a problem")
    else:
        raise HTTPException(status_code=400, detail=f"Cannot upload {file.filename}")

@router.post("/tokenize")
async def sys_turn_into_token(file_name:str):
    result, is_successful = global_st.extract_into_txt(file_name=file_name)
    if is_successful:
        return {"detail": result}
    elif result == "Not found":
        raise HTTPException(status_code=400, detail=f"Not found {file_name}")
    else:
        raise HTTPException(status_code=500, detail=f"Service Unavailable, Storage has a problem")
  
@router.delete("/delete-file")
async def sys_delete_file(file_name:str):
    
    if check_existing(name=file_name, in_corpus=True) and check_existing(name=file_name, in_corpus=False):
        is_successful, result = global_st.delete_blob(blob_name=file_name, in_corpus=True)
        if not is_successful:
            raise HTTPException(status_code=503, detail=f"Service Unavailable, Google storage has a problem")
        else:
            return {"detail": f"Delete file {file_name} successfully"}
    elif check_existing(name=file_name, in_corpus=False):
        is_successful, result = global_st.delete_blob(blob_name=file_name, in_corpus=False)
        if not is_successful:
            raise HTTPException(status_code=503, detail=f"Service Unavailable, Google storage has a problem")
        else:
            return {"detail": f"Delete file {file_name} successfully"}
    else:
        raise HTTPException(status_code=400, detail=f"{file_name} is not existing")
        
@router.delete("/delete-folder")
async def sys_delete_folder(folder_name:str):
    
    
    if check_existing(name=folder_name, in_corpus=True, is_folder=True) and check_existing(name=folder_name, in_corpus=False, is_folder=True):
        is_successful, result = global_st.delete_folder(folder_name=folder_name)
        if not is_successful:
            
            raise HTTPException(status_code=503, detail=f"Service Unavailable, Google storage has a problem")
        else:
            return {"detail": f"Delete folder {folder_name} successfully"}
    else:
        raise HTTPException(status_code=400, detail=f"{folder_name} is not existing")    
    
# TODO: PUT -> safe state file
@router.put("/save-file")
async def sys_save_status_file(file:UploadFile, tagset_id:int):
    
    #// Send text to endpoint API (string)
    #// Save file
    
    pass

@router.put("/change-blob-name", status_code=200)
async def sys_rename_file(old_name:str, new_name:str):
    
    #//Check is th blob in th corpus as well
    if old_name != new_name:
        if check_existing(name=old_name, in_corpus=True) and check_existing(name=old_name, in_corpus=False):
        
            is_successful, result = global_st.rename_blob(old_name=old_name, new_name=new_name, in_corpus=True)
            if not is_successful:
                raise HTTPException(status_code=503, detail=f"Service Unavailable, Google storage has a problem")
            else:
                return {"detail": f"Rename file successfully"}
            
        elif check_existing(name=old_name, in_corpus=False):
            is_successful, result = global_st.rename_blob(old_name=old_name, new_name=new_name, in_corpus=False)
            if not is_successful:
                raise HTTPException(status_code=503, detail=f"Service Unavailable, Google storage has a problem")
            else:
                return {"detail": f"Rename file successfully"}
            
        else:
            raise HTTPException(status_code=400, detail=f"{old_name} is not existing")
    else:   
        raise HTTPException(status_code=400, detail=f"The old name and new name is the same")

@router.put("/change-folder-name", status_code=200)
async def sys_rename_folder(old_name:str, new_name:str):
    
    if old_name != new_name:
        if validate_folder_name(name=new_name):
            if check_existing(name=old_name, in_corpus=False):
                is_successful, result = global_st.rename_folder(old_name=old_name, new_name=new_name)
                
                if not is_successful:
                    raise HTTPException(status_code=503, detail=f"Service Unavailable, Storage has a problem")
                else:
                    return {"detail":"Rename folder successfully"}

            else:
                raise HTTPException(status_code=400, detail=f"No path {old_name}")
        else:
            raise HTTPException(status_code=400, detail=f"{old_name} is not existing")
    else:
        raise HTTPException(status_code=400, detail=f"The old name and new name is the same")