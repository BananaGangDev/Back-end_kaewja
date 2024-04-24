from fastapi import HTTPException,status
from google.cloud import storage
#from google.cloud import bigquery
from io import StringIO
import csv
from src.connections import Storage 
from src.connections import global_st
from src.concordancer.schemas import requestSchema
from nltk.tokenize import word_tokenize

MAX_LEN = 100 #Maximum string per len

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
        filenames.append(path)
    
    return {"filename":filenames}
        
def get_path_by_filename(input):
    json_path = get_all_filename()
    filenames = set(list(json_path.values())[0])
    # print(filenames)
    input = set(input)
    correct_filenames = list(input.intersection(filenames))
    return {"filename":correct_filenames}

def get_string(filename):
    blob = global_st.global_corpus.blob(filename)
    blob = blob.download_as_text()
    return blob

def get_all_words():
    json_path = list(get_all_filename().values())[0]
    for path in json_path:
        essay = get_string(path).replace("\r\n\r\n",". ")
        count = len(word_tokenize(essay))
        return count
        
def get_right_side(words,index):
    count = 0
    location = index
    str_right = ""
    while (count < MAX_LEN) and (location > 0) :
        location -= 1
        word = words[location]
        len_word = len(words[location])
        if (count + len_word) > MAX_LEN :
            break
        else :
            str_right = word + " " + str_right
            count = len(str_right)
        
    print(str_right,count)
    return str_right

def get_left_side(words,index):
    count = 0
    location = index
    str_left = ""
    # print(len(words),location)
    while (count < MAX_LEN) and ((len(words)-location) > 1) :
        location += 1
        # print(len(words),location)
        word = words[location]
        len_word = len(words[location])
        if (count + len_word) > MAX_LEN :
            break
        else :
            str_left = str_left + " " + word
            count = len(str_left)
    print(str_left,count)
    return str_left
            
            
        