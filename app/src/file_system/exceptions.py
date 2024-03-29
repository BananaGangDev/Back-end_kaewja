import re
from src.connections import global_st

#// Check folder name
def validate_folder_name(name:str):
    pattern = r'^[^\\\\/?%*:|"<>.]+$' #// wrong pattern
    
    if name.count("/") == 0:
        return bool(re.match(pattern, name))

    else:
        if name.count("/") <= 1 and name.count("/") > 0: 
            folders = name.split("/")
            num = 0
            for i in folders:
                if bool(re.match(pattern, i)):
                    num +=1
            if num == len(folders):
                return True
                    

def validate_file():
    #// .pdf .txt .doc
    pass    
    

def check_existing(name:str, in_corpus:bool=False, is_folder:bool=False):
    
    
    if not in_corpus and not is_folder:
        result, paths = global_st.get_all_path_files(in_corpus=in_corpus)
    else:
        name = name[:len(name)-4] + ".txt" #// a.pdf -> a.txt\
        result, paths = global_st.get_all_path_files(in_corpus=in_corpus)
    
    for path in paths:
        if path.startswith(name):
            return True
        
    return False