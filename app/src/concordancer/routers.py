from fastapi import APIRouter

router = APIRouter(
    tags=["Concordancer"]
)

# ส่งค่าให้
# {
#  "pointFocus" : "คำที่ต้องการsearch",
# }
# ต้องการรับค่า
# {
# "Data" : [[file_name , leftcontext, rightcontext]
# ]
# "information": [จำนวนทั้งหมดที่ได้จากการsearch, peromillion, percent]
# len ที่สามารถรองรับได้ = 110 ( ตัวอักษร+space)
# }

