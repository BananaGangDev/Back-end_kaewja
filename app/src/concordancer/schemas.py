# 2nd ORM
from pydantic import BaseModel
from typing import List

class requestSchema(BaseModel):
    point_focus : str 
    filename : List
    
class DataToken(BaseModel):
    data : List #List ของ data
    searching_num : int #จำนวนประโยคที่มีคำนั้น
    per_million : float #จำนวนต่อล้าน
    percent : float #จำนวนต่อร้อย