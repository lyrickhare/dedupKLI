#!/usr/bin/env python
# coding: utf-8

# In[5]:


import os
import pathlib
from pathlib import Path
import sys  
sys.path.insert(0, '../main/classify')
import segregate
sys.path.insert(0,'../main/dedup')
import bestquality
import shutil


# In[6]:


def main(path, path1):
    
    os.mkdir(path1)

    proposal_list = os.listdir(path)

    for i in proposal_list:
        path_final = path1 + '/' + i
        os.mkdir(Path(path_final))
    for i in os.listdir(path1):
        path_Aadhaar = path1+'/'+i+'/Aadhaar'
        path_PAN = path1+'/'+i+'/PAN'
        path_other = path1+'/'+i+'/other'
        path_DL = path1+'/'+i+'/DL'
        path_Passport = path1+'/'+i+'/Passport'
        os.mkdir(path_Aadhaar)
        os.mkdir(path_PAN)
        os.mkdir(path_other)
        os.mkdir(path_DL)
        os.mkdir(path_Passport)
    myFolder = list()
    pos = 0
    list_new = os.listdir(path1)
    for dirname in os.listdir(path):
        f = os.path.join(path,dirname)
        if os.path.isdir(f):
            myFolder.append(f)
    for folder in myFolder:
        img_file = list(Path(folder).rglob("*"))
        img_file1 = [str(i) for i in img_file]
        dict1 = segregate.segregate(img_file1)
        dict2 = bestquality.bestquality(dict1)
        dict2 = {i:j for i,j in dict2.items() if j != ['']}
        for j in os.listdir(path1+'/'+list_new[pos]):
            for k in dict2:
                if(j==k):
                    shutil.copy(Path(str(dict2[k]).replace("[","").replace("]","").replace("'","")),Path(path1+'/'+list_new[pos]+'/'+j))
        pos = pos + 1
    [os.removedirs(p) for p in Path(path1).glob('**/*') if p.is_dir() and len(list(p.iterdir())) == 0]


# In[ ]:




