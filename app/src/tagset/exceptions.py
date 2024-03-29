import re
from .crud import get_tagset_by_id

def check_name(name: str):
    pattern = r"^[a-zA-Z]"
    return bool(re.match(pattern, name))

def validate_format_datetime(answers:list, datetime_format) -> bool:
    pattern = re.compile(datetime_format)
    is_correct = True
    for i in answers:
        if not (bool(re.match(pattern, i))):
            is_correct = False
    return is_correct


def check_tagset_existing(tagset_name:str, tagset_id:int,db):
    
    find_tagset = get_tagset_by_id(tagset=tagset_id, db=db)
    if not find_tagset:
        return False
    
    else:
        if find_tagset.tagset_name == tagset_name:
            return True
        else:
            return False
    