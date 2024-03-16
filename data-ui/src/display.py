from typing import Any, Dict,List
import json
import os

mode_option={"mode1":List[Dict],"mode2":Dict}

class JsonDisplay(object):
    def __init__(self,mode,path,id=0) -> None:
        self.mode=mode
        self.path=path
        self.id=id

        self.init()

    def init(self):
        assert self.mode in mode_option.keys(),f"mode is not right,mode should be in {mode_option}."
        assert os.path.exists(self.path)==True,f"{self.path} does not exists."

    def readJsonFile(self):
        if self.mode=="mode1":
            return self._readJson()
        elif self.mode=="mode2":
            return self._readJsonLines()
        else:
            raise NotImplemented(f"{self.mode} is not in {mode_option}")


    def _readJson(self)->List[Dict]:
        with open(self.path,"r",encoding="utf-8") as f:
            content=json.load(f)
        return content
    
    def _readJsonLines(self)->List[Dict]:
        total_data=[]
        with open(self.path,"r",encoding="utf-8") as f:
            for line in f:
                # print(line)
                data=json.loads(line)
                total_data.append(data)
        return total_data
    
    def showOneData(self):
        data=self.readJsonFile()
        assert self.id in range(len(data)),f"{self.id} is not right."
        return data[self.id]
    
    def return_total_data(self)->List[Dict]:
        data=self.readJsonFile()
        return data
    
    