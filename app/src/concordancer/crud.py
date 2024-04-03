from fastapi import HTTPException,status
from google.cloud import storage
#from google.cloud import bigquery
from io import StringIO
import csv
from src.connections import Storage 
from src.connections import global_st
from src.concordancer.schemas import requestSchema
from nltk.tokenize import word_tokenize

PATH = "level999"

def check_filename(filenames):
    json_path = get_all_filename()
    if len(filenames) > 1 :
        for filename in filenames:
            if filename in json_path["filename"]:
                return get_path_by_filename(filenames,json_path)
            elif len(filenames) == 1 and filenames[0]=="all":
                return json_path
            else : 
                return False
        
def get_all_filename():
    paths = Storage.get_all_path_files(global_st,in_corpus=True)[1]
    filenames = []
    for path in paths:
        folder,filename = path.split('/')
        if folder == PATH:
            filenames.append(filename)
    
    return {"filename":filenames}
        
def get_path_by_filename(input):
    json_path = get_all_filename()
    filenames = set(list(json_path.values())[0])
    # print(filenames)
    input = set(input)
    correct_filenames = list(input.intersection(filenames))
    return {"filename":correct_filenames}

def get_string(filename):
    blob = global_st.global_corpus.blob(PATH + "/" + filename)
    blob = blob.download_as_text()
    return blob

def get_all_words():
    json_path = list(get_all_filename().values())[0]
    for path in json_path:
        essay = get_string(path).replace("\r\n\r\n",". ")
        count = len(word_tokenize(essay))
        return count
        
    