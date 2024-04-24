from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from src.concordancer import crud
from src.connections import global_st
from src.concordancer.schemas import requestSchema,DataToken
import nltk
from nltk.tokenize import sent_tokenize,word_tokenize

router = APIRouter(
    prefix="/concordancer",
    tags=["Concordancer"]
)

nltk.download('punkt')
nltk.download('stopwords')

STR_LEN = 30 #Maximum string per len
        
@router.get("/get_filename",status_code=200)
def get_filename():
    return crud.get_all_filename()

@router.post("/concordancer",status_code=200)
def get_concor(point_focus:str , filenames:List[str]):
    focus_count = 0 
    data = []
    json_path = crud.get_path_by_filename(filenames).values()
    # print(json_path)
    if json_path:
        value = list(json_path)[0]
        for path in value:
            essay = crud.get_string(filename=path)
            essay = essay.replace("\r\n\r\n",". ")
            sentences = sent_tokenize(essay)
            for sentence in sentences:
                words = word_tokenize(sentence)
                #print(words)
                if (point_focus in words) and (words.count(point_focus)>0):
                    for word in words:
                        if word == point_focus:
                            index = words.index(point_focus)
                            data.append([path,' '.join(words[0:index]),' '.join(words[index+1:len(words)+1])])
                            focus_count +=1
        
        if focus_count == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No word in corpus. Please refill a new word.")
        else:
            all_words = crud.get_all_words()
            percent = focus_count/all_words
            return {
                "pointFocus":point_focus,
                "Data":data,
                "num_words":focus_count,
                "permillion": percent*(10**6),
                "percent": percent
            }
        
    else : 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No filename in our bucket. Please refill a new filename.")
                