from logger import Logger
import json
import requests
from urllib.parse import quote
from file_tool import File_Tool
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class TianYanService:
    def __init__(self):
        self.logging = Logger().get_log()
        self.search_url = "https://capi.tianyancha.com/cloud-tempest/app/searchCompany"
        self.info_url = "https://api9.tianyancha.com/services/v3/t/details/appComIcV4/{{}}?pageSize=1000"
        self.fileTool = File_Tool()
        self.fileTool.initTianyan()
        self.BASE_HEADER ={
            'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.6(0x18000633) NetType/WIFI Language/zh_CN",
            'Authorization': '0###oo34J0R8wkBC6K48XWfXarynHiAg###1632836312164###db42a2099bea3d479e66e23fb1fbf81d',
            'version':'TYC-XCX-WX',
            "content-type":"application/json;charset=UTF-8"
        }
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def get_company_list(self):
        cmps = self.fileTool.readTianyanCompanys("./cmps.csv")
        i = 0
        for cmp in cmps:
            i += 1
            if i < 434:
                continue
            self.search_cmp_id(cmp)
            print("no:"+str(i))
        #print(len(cmps))

    def search_cmp_id(self,name):
        name= str(name).replace("\n","")
        data = {"sortType":0,"pageSize":1,"pageNum":1,"word":name,"allowModifyQuery":1}
        data_json = json.dumps(data) 
        response = requests.post(url = self.search_url, data=data_json, headers=self.BASE_HEADER, timeout=20,verify=False)
        #print(response.text)
        response_json = json.loads(response.text)
        cmp = response_json.get("data").get("companyList")[0]
        if cmp:
            cmp_name = cmp.get("name")
            cmp_id = cmp.get("id")
            self.logging.info(cmp_name+str(cmp_id))
            #return {"id":cmp_id,"name":cmp_name}
            if name in str(cmp_name):
                self.fileTool.updateTianyanCmpId(name,cmp_id)
            else:
                self.fileTool.errorTianyanCmp(name+","+cmp_name+","+str(cmp_id))
        else:
            self.fileTool.errorTianyanCmp(name)

    def read_cmpid(self):
        cmpids = self.fileTool.readTianyanCompanys("./cmp.index")
        if cmpids:
            i = 0
            for cmpid in cmpids:
                #if i > 3:
                #    return
                i += 1
                print("start no="+str(i))
                self.logging.info(cmpid)
                cmpida = str(cmpid).split(",")
                if len(cmpida) == 2:
                    name = cmpida[0]
                    id = cmpida[1]
                    id = str(id).replace("\n","")
                    self.get_cmp_info(name,id)
                else:
                    self.fileTool.errorTianyanCmp(cmpid)

    def get_cmp_info(self,name,id):
        _url = self.info_url.replace("{{}}",id)
        self.logging.info(_url)
        response = requests.get(url = _url, headers=self.BASE_HEADER, timeout=20,verify=False)
        #print(response.text)
        response_json = json.loads(response.text)
        cmp = response_json.get("data").get("baseInfo")
        if cmp:
            js = json.dumps(cmp)
            self.fileTool.writeTianyanJson(js)
            reg = cmp.get("regInstitute")
            self.fileTool.writeTianyanResult(name,reg)
        else:
            self.fileTool.errorTianyanCmp2(name,id)

if __name__ == "__main__":
    tianyan = TianYanService()
    tianyan.get_company_list()
    tianyan.read_cmpid()

