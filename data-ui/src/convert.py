import pandas as pd
from typing import List,Dict
from datetime import datetime
import os

def show(data_lst):
    string=""
    for data in data_lst:
        string+=data+"\n"
    return string


class DataConvertXlsx(object):
    def __init__(self,data_lst:List[Dict],is_show_detail:bool) -> None:
        self.data_lst=data_lst
        self.is_show_detail=is_show_detail

    def convert2xlsx(self)->pd.DataFrame:
        total_data=[]
        column_names=list(self.data_lst[0].keys())
        for data_dict in self.data_lst:
            one_data_dict={}
            for col in column_names:
                val=data_dict[col]
                if isinstance(val,list) and isinstance(val[0],str) and self.is_show_detail:
                    question=val[0].split("\n")[-1]
                    system=val[0].replace(question,"").strip()
                    one_data_dict["system_template"]=system
                    one_data_dict["query"]=question
                    one_data_dict["trajectory"]=show(val[1:])
                one_data_dict[col]=val
            total_data.append(one_data_dict)
        df=pd.DataFrame(total_data)
        return df
    
    def save(self,save_file_format,save_path='.'):
        df=self.convert2xlsx()
        now = datetime.now()
        formatted_now = now.strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"{formatted_now}"
        if save_file_format=="csv":
            file_name+=".csv"
            output_file=os.path.join(save_path,file_name)
            df.to_csv(output_file,index=False)
        elif save_file_format=="xlsx":
            file_name+=".xlsx"
            output_file=os.path.join(save_path,file_name)
            df.to_excel(output_file,index=False)
        else:
            raise ValueError("option should be ['csv','xlsx']")
        return output_file

            
            



        

        