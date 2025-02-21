#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import chardet
import sys
import re

CXX_FILES=[".h",".c",".hh",".cc",".hpp",".cpp",".hxx",".cxx",".ipp",".inl",".inc"]

def is_cxx_file(file):
    name,ext = os.path.splitext(file)
    return ext.lower() in CXX_FILES

def gbk_to_utf8(des_file, res_file):
    with open(des_file,'rb') as f:
        data = f.read()
    
    res = chardet.detect(data)
    if res['encoding'] == 'GB2312':
        res['encoding'] = 'GBK'
        
    with open(res_file,'w',encoding='utf-8') as file:
        line =str(data,encoding=res['encoding'])
        file.write(line)
    
def has_chinese(line):
    result = re.compile(u'[\u4e00-\u9fa5]')
    if result.search(line):
        return True
    return False
    
def process_dir(dir):
    
    for root,dirs,files in os.walk(dir):
        for file in files:
            if not is_cxx_file(file):
                continue
            
            fullpath = os.path.join(root,file)
            print(f"处理文件:{fullpath}")
            has_changed = False
            # gbk_to_utf8(fullpath,fullpath)
            wlines = []
            try:
                with open(fullpath,encoding='utf-8') as f:
                    for line in f.readlines():
                        if line.find("//") >= 0 and has_chinese(line):
                            line = line.replace("//","/* ")
                            line = line.rstrip() + "*/\n"
                            wlines.append(line)
                            has_changed = True
                        else:
                            wlines.append(line)
                            
            except:
                print(f"处理文件出错:{fullpath}")
                wlines=[]
                continue
            
            if has_changed:
                with open(fullpath,'w',encoding='utf-8') as f:
                    f.writelines(wlines)
                

                        
if __name__ == "__main__":
    process_dir(sys.argv[1])
