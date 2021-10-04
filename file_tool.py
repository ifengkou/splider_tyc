# -*- coding: utf-8 -*-
import os

class File_Tool:
    def writeFile(self, save_path,content):
        with open(save_path, 'w') as f:
            f.write(content)
            
    def createFile(self, save_path, filename):
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_path = os.path.join(save_path, filename)
        if not os.path.exists(file_path):
            _file = open(file_path, 'a+')
            _file.close()
            return file_path
        else:
            # 已存在同名文件
            return ''

    def readTianyanCompanys(self,filePath):
        with open(filePath, 'r') as f:
            return f.readlines()

    def initTianyan(self):
        self.createFile("./","cmp.index")
        self.createFile("./","result.csv")
        self.createFile("./","error.txt")
        #self.createFile("./","result.json")
        self.createFile("./","error_info.txt")
    
    def updateTianyanCmpId(self,company,id):
        with open("./cmp.index", 'a') as f:
            f.write(company+","+str(id)+"\n")
    
    def errorTianyanCmp(self,company):
        with open("./error.txt", 'a') as f:
            f.write(company+"\n")

    def errorTianyanCmp2(self,company,id):
        with open("./error_info.txt", 'a') as f:
            f.write(company+","+str(id)+"\n")

    def writeTianyanResult(self,company,reg):
        with open("./result.csv", 'a') as f:
            f.write(company+","+reg +"\n")

    def writeTianyanJson(self,js):
        with open("./result.json", 'a') as f:
            f.write(js +"\n")

    def two_in_one(self):
        flist=[]
        with open("./cmp.index", 'r') as f:
             flist= f.readlines()
        i = 1
        newlines = []
        for line in flist:
            if i%2 == 1:
                newline= str(line).replace("\n","")
            if i%2 == 0:
                newline = newline + line
                newlines.append(newline)
            i += 1
        with open("./xxx.txt", 'w') as f:
            f.writelines(newlines)
