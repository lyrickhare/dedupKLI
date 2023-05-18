#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os
import pathlib
from pathlib import Path
import sys  
# sys.path.insert(0, '../main/classify')
import segregate
# sys.path.insert(0,'../main/dedup')
import bestquality
import shutil


# In[2]:




# In[4]:

#Building Main Function

def main(src_path, dest_path):
    #Dictionary to store count:
    dict_count = {'Total Proposals': 0, 'Images Processed': 0, 'Duplicate Images': 0, 'Documents recognized': 0, 'Images Saved':0, 'Other Files':0}
    #Creating an empty folder to store indexed images of each proposal:
    os.mkdir(dest_path)
    #Fetching proposal ids:
    proposal_list = os.listdir(src_path)
    #Getting total no. of proposals:
    dict_count['Total Proposals'] = len(proposal_list)
    #Creating an empty folder for each proposal id in the destination path:
    for i in proposal_list:
        path_final = dest_path + '/' + i
        os.mkdir(Path(path_final))
    #Creating folder for each document:
    for i in os.listdir(dest_path):
        path_Aadhaar = dest_path+'/'+i+'/Aadhaar'
        path_PAN = dest_path+'/'+i+'/PAN'
        path_other = dest_path+'/'+i+'/other'
        path_DL = dest_path+'/'+i+'/DL'
        path_Passport = dest_path+'/'+i+'/Passport'
        os.mkdir(path_Aadhaar)
        os.mkdir(path_PAN)
        os.mkdir(path_other)
        os.mkdir(path_DL)
        os.mkdir(path_Passport)
    myFolder = list()
    pos = 0
    list_new = os.listdir(dest_path) #Fetches names of proposal ids created in destination folder
    #Getting the path of each proposal id folder:
    for dirname in os.listdir(src_path):
        f = os.path.join(src_path,dirname)
        if os.path.isdir(f):
            myFolder.append(f)
    #Fetching path of images and passing it to the functions segregate and bestquality for classification & deduplication:
    for folder in myFolder:
        img_file = list(Path(folder).rglob("*"))
        img_file1 = [str(i) for i in img_file]
        segregated_dict = segregate.segregate(img_file1) #Getting the classified dictionary
        dict_count['Images Processed']+=sum(map(len, segregated_dict.values())) #Counting total no. of images
        final_dedup_dict = bestquality.bestquality(segregated_dict) #Getting the de-duplicated dictionary
        final_dedup_dict = {i:j for i,j in final_dedup_dict.items() if j != ['']} #Removing null items
        print(final_dedup_dict)
        dict_count['Images Saved']+=sum(map(len, final_dedup_dict.values())) #Couting no. of images that are saved
        for i in final_dedup_dict:
            if(i=='other'):
                dict_count['Other Files']+=len(final_dedup_dict['other'])   #Counting no. of other images
        #Copying images from source path to the final indexed folder for each proposal id:
        for j in os.listdir(dest_path+'/'+list_new[pos]):
            for k in final_dedup_dict:
                if(j!='other' and k!='other' and j==k):
                    shutil.copy(Path(str(final_dedup_dict[k]).replace("[","").replace("]","").replace("'","")),Path(dest_path+'/'+list_new[pos]+'/'+j))
                elif(j==k and k=='other' and final_dedup_dict['other']!=[]):
                    other_list = str(final_dedup_dict['other']).split(',')
                    for l in other_list:
                        shutil.copy(Path(str(l).replace("[","").replace("]","").replace("'","").replace(" ","")),Path(dest_path+'/'+list_new[pos]+'/'+j))
        pos = pos + 1
    [os.removedirs(p) for p in Path(dest_path).glob('**/*') if p.is_dir() and len(list(p.iterdir())) == 0] #Deleting indexed folders that are empty
    dict_count['Duplicate Images'] = dict_count['Images Processed'] - dict_count['Images Saved']
    dict_count['Documents recognized'] = dict_count['Images Saved'] - dict_count['Other Files']
    for key, value in dict_count.items():
        print(key, ' : ', value)
    dict_count.clear()


# In[ ]:




