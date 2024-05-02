from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import false, or_ 
from src.dashboard import schemas
from src.connections import global_db,global_st
import re
from src.tagset import crud as tagset_crud
from src.dashboard import crud as dashboard_crud
from typing import Annotated
# from src.file_system.routers import all_uncleaned_paths
# from bigtree import Node,dataframe_to_tree
import pandas as pd
import cProfile
import pstats


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

def get_db():
    db = global_db.get_sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/create_stat",status_code=201)
def create_stat(string,tagset_id,filename,db:db_dependency):
        # label = get_label_in_tagset(tagset=int(tagset_id),db=db)[0]
        tags = re.findall(r'<[^<>]+>',string)
        if tags:
            count_tags = len(tags)
            # print(count_tags)
            stat_dicts = {}
            for i in range(0,len(tags)-1,2):
                if (tags[i][0] == "<") and (tags[i][-1] == ">"):
                    front_tag = tags[i].split()[0][1:3]
                    back_tag = tags[i+1]
                    # print(front_tag,back_tag)
                    label = dashboard_crud.check_label_by_label_name(db=db,label_name=front_tag,tagset_id=tagset_id)
                    if (front_tag in back_tag) and label:
                        # print(label)
                        if front_tag not in stat_dicts.keys():
                            stat_dicts[front_tag] = {"count":1,"label_id":int(label.label_id)}
                        else : 
                            stat_dicts[front_tag]["count"] += 1
                            
            count = len(stat_dicts)
            for key,value in stat_dicts.items():
                print(key,value)
                # result = check_label_by_file(db=db,filename=filename,label_id=dict["label_id"])
                if dashboard_crud.check_label_by_file(db=db,filename=filename,label_id=value["label_id"]):
                    data = dashboard_crud.update_data(db=db,filename=filename,tagset_id=int(tagset_id),label_id=value['label_id'],new_count=value['count'])
                    count -= 1
                else : 
                    data = dashboard_crud.add_data(db=db,filename=filename,tagset_id=tagset_id,label_id=value['label_id'],count=value['count'])
                    count -= 1
            return Response(content="update dashboard successfully",status_code=status.HTTP_201_CREATED)
        else:
            return Response(content="No tag in this file",status_code=status.HTTP_204_NO_CONTENT)

#Get Summary Stat        
@router.get("/get_stat",status_code=200)
def get_stat(tagset_id,db:db_dependency):
    is_successful,file = global_st.get_all_path_files(in_corpus=False)
    total_document = len(file)
    checked_document = dashboard_crud.get_stat_by_id(db=db,tagset_id=tagset_id)
    roots = dashboard_crud.get_label_by_root(db=db,tagset_id=tagset_id,label_level=0,label_parent="ROOT")
    print(checked_document)
    print(roots)
    if (checked_document in [[],False,None]) or (roots in [[],None,False]):
        return Response(content="No data",status_code=status.HTTP_204_NO_CONTENT)
    
    path = []
    for root in roots:
        string_root = root.label_name
        all_level1 = dashboard_crud.get_label_by_root(db=db,tagset_id=tagset_id,label_parent=root.label_name,label_level=1)
        if all_level1:
            for level1 in all_level1:
                string_level1 = string_root + "/" + level1.label_name
                all_level2 = dashboard_crud.get_label_by_root(db=db,tagset_id=tagset_id,label_parent=level1.label_name,label_level=2)
                if all_level2 :
                    for level2 in all_level2:
                        string_level2 = string_level1 + "/" + level2.label_name
                        all_level3 = dashboard_crud.get_label_by_root(db=db,tagset_id=tagset_id,label_parent=level2.label_name,label_level=3)
                        if all_level3 :
                            for level3 in all_level3:
                                string_level3 = string_level2 + "/" + level3.label_name
                                path.append([string_level3,0])
                        else:
                            path.append([string_level2,0])
                else:
                    path.append([string_level1,0])
        else:
            path.append([string_root,0])
                            
    df_labels = pd.DataFrame(path,columns=["PATH","Count"])
    for stat in checked_document:
        label = dashboard_crud.get_label_by_label_id(db=db,label_id=stat.label_id)
        label_name = label.label_name
        count = stat.count
        # print(label_name)
        for path in df_labels['PATH']:
            full_path = path
            if '/' in path:
                path = path.split('/')[-1]
                # print(label_name)
                # print(path)
            
            if label_name == path:
                new_value = df_labels['Count'].loc[(df_labels['PATH']==full_path)] + count
                # print(df_labels.loc[(df_labels['PATH']==full_path)]['Count'])
                df_labels['Count'].loc[(df_labels['PATH']==full_path)] = new_value
    
    raw_df = df_labels.loc[df_labels['Count'] > 0]
    # print(raw_df)
    root_names = []
    all_count = 0
    for index in raw_df.index.values.tolist() :
        # print(df)
        #print(raw_df['PATH'].loc[(raw_df.index==index)])
        tmp = raw_df['PATH']
        root = tmp[index].split('/')[0]
        if root not in root_names :
            root_names.append(root)
        all_count+=raw_df['Count'][index]
    
    data = []
    
    for root_name in root_names:
        child_data = [] 
        for index in raw_df.index.values.tolist() :
            tmp = raw_df['PATH']
            root_tmp = tmp[index].split('/')[0]
            child_name = tmp[index].split('/')[-1]
            if root_tmp == root_name:
                # child = dashboard_crud.get_label_by_label_name(db=db,label_name=child_name)
                # print(raw_df['Count'][index],type(raw_df['Count'][index]))
                # percent = (raw_df['Count'][index].item()/all_count)*100
                count = raw_df['Count'][index].item()
                json = {
                    "child_name" : child_name,
                    "child_description" : dashboard_crud.get_label_description(db=db,label_name=child_name),
                    "count" : count,
                    "percent" : str((count/all_count)*100)
                }
                child_data.append(json)
        
        data.append({
            "root_name" : root_name,
            "data" : child_data
        })
    
    card_data = {
        "total" : str(total_document),
        "check" : str(len(checked_document)),
        "error" : str(all_count)
    }
    
    output = {"card_data":card_data,
            "data":data
    }
    return output

#Get Stat Card In DB
@router.get("/get_stat_from_db",status_code=200)
def get_stat_by_id(tagset_id,db:db_dependency):
    return dashboard_crud.get_stat_by_id(db=db,tagset_id=tagset_id)