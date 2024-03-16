from .display import JsonDisplay
from .convert import DataConvertXlsx

import os


def show_data_by_id(mode,json_file,id):
    jd=JsonDisplay(mode,json_file,int(id))
    one_data=jd.showOneData()
    return one_data

def show_data_detail(mode,json_file,id):
    def show_list(data_lst):
        string=""
        for data in data_lst:
            string+=data+"\n"
        return string
    
    jd=JsonDisplay(mode,json_file,int(id))
    one_data=jd.showOneData()

    print(one_data)
    total_string="###SYSTEM###"
    keys_lst=list(one_data.keys())
    for key in keys_lst:
        val=one_data[key]
        if isinstance(val,list) and isinstance(val[0],str):
            question=val[0].split("\n")[-1]
            system=val[0].replace(question,"").strip()
            total_string+="\n\n"+system+"\n\n"
            total_string+="###Trajectory###"+"\n\n"+question
            string=show_list(val[1:])
            total_string+="\n\n"+string
    print(total_string)
    return total_string


def convert_json_data(mode,json_file,save_file_format,save_path="."):
    try:
        jd=JsonDisplay(mode,json_file)
        total_data=jd.return_total_data()
        convert=DataConvertXlsx(data_lst=total_data,is_show_detail=True)
        path=convert.save(save_file_format,save_path)
        msg=f"保存的数据格式：{save_file_format},保存路径{path}"
    except Exception as error:
        msg=str(error)
        msg+="\n\n"+"处理出错"
    return msg

    

    


