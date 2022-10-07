#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:时无ShiWu
#Filename:story_jp_rs.py
#Version:1.0

import os
import pandas as pd
import json
import difflib
import sys

# 字符串定义
aud_normal='VO_CHR_INGAMESTORY_00_00_0000'
ori_path=os.path.split(os.path.realpath(__file__))[0]
char_id=f'{ori_path}/char_id.csv'
filepath=f'{ori_path}/queststory_main'
filelist=f'{ori_path}/queststory_main.csv'
export_path=f'{ori_path}/queststory_main_jp'
mainstory_fnmae=''
print(ori_path)

# 判断字符串相似度
def str_eqrate(str1,str2):
    return difflib.SequenceMatcher(None,str1,str2).quick_ratio()

# 加载charaid表
cidfile=pd.read_csv(char_id)
cidlen=len(cidfile['cid'])
# 导入剧情文件列表
eachfile=pd.read_csv(filelist)
eflen=len(eachfile['filename'])
# eflen=1 # 测试用
fname=''
for i in range(0,eflen):
    fname=eachfile['filename'][i]
    # fname='1000001' # 测试用

    # 加载主线剧情json文件
    s0json=f'{filepath}/{fname}.json'
    with open(s0json,'r',encoding='utf-8') as story0j:
        mainstory=json.load(story0j)
        mainstory=dict(mainstory)
    sjl=len(mainstory['functions'])
    nlze=pd.json_normalize(mainstory['functions'][0],'commandList')
    pd.set_option('display.max_rows',None)
    # nlze.to_csv(ori_path+f'/queststory_main_csv/{fname}.csv',encoding='utf-8_sig')

    # json结构<已作废，备查>
    # ['name','args','defaultValues',['commandList','row'],['commandList','command'],['commandList','args'],['commandList','end']]
    # ['variables','buckets'],['variables','count'],['variables','entriesHashCode'],['variables','entriesNext'],['variables','entriesKey'],['variables','entriesValue'],['variables','freeCount'],['variables','freeList']

    # 获取列长度
    nlzelen=len(nlze['row'])
    # 定义剧情概要、演员角色、台词、台词暂存变量
    role=[]
    rolew=[]
    rwtemp=''
    # 剧情概要、角色台词开始标志、变量
    outline=0
    start=0
    oltitle=''
    oltext=''
    no_audio=1
    for i in range(0,nlzelen):
        # 剧情概要处理
        if(nlze['command'][i]=='OL_TITLE'):
            outline=1
            oltitle=nlze['args'][i]
        # 剧情概要文本拼接
        if(nlze['command'][i]=='outline'):
            if outline==1:
                outlen=len(nlze['args'][i])
                for g in range(0,outlen):
                    if('\\n' in nlze['args'][i][g]):
                        oltemp=str(nlze['args'][i][g])
                        oltemp.replace('\\n','\n')
                    elif(nlze['args'][i][g]=='block_a' or nlze['args'][i][g]=='end_block'):
                        # print('ol_title end')
                        outline=0
                        oltext=oltext.replace('\\n','\n')+'\n\n'
                    else:
                        oltext=oltext+nlze['args'][i][g]
        if(start==0 and nlze['command'][i]=='ruby'):
            oltext=oltext+nlze['args'][i][0]
        # 对话处理
        if(nlze['command'][i]=='WFIN_SHORT' or nlze['command'][i]=='window_type'):
            start=1
        # if start==1:
        if(nlze['command'][i]=='print'):
            if start==1:
                arglen=len(nlze['args'][i])
                for j in range(0,arglen):
                    if 'player_name' in nlze['args'][i][j]:
                        rpn='王子' #ユーディル
                    # 当人物id包含#cn时，替换为空白
                    if '#cn' in nlze['args'][i][j]:
                        rpn=str(nlze['args'][i][j])
                        rpn=rpn[0:rpn.rfind('#')]
                    # 当人物id包含#时，替换为空白
                    elif '#' in nlze['args'][i][j]:
                        rpn=str(nlze['args'][i][j])
                        rpn=rpn[0:rpn.rfind('#')]
                    # 当人物id字母部分只有cn时，对照char_id.csv查表
                    elif 'cn' in nlze['args'][i][j]:
                        rpn=str(nlze['args'][i][j])
                        for b in range(0,cidlen):
                            if(rpn==cidfile['cid'][b]):
                                rpn=cidfile['jp'][b]
                    # 避免换行符出现在句子前导致文本无法正常换行
                    elif '\\n' in str(nlze['args'][i][j])[0:2]:
                        if('#' in nlze['args'][i][j] or 'cn' in nlze['args'][i][j]):
                            rpn=str(nlze['args'][i][j])
                            rpn=rpn[0:rpn.rfind('#')]
                    # 当print内容出现了音频播放时，输出音频播放内容
                    # 结束标识符出现时将角色名称和台词写入列表
                    elif str_eqrate(nlze['args'][i][j],aud_normal)>0.72:
                        if start==1:
                            role.append(rpn)
                            rwtemp=rwtemp.replace('\\n','\n')
                            rwlen=len(rwtemp)
                            if(rwlen>3 and '\\n' not in rwtemp[-2]):
                                rwtemp=rwtemp+'\n'
                            rolew.append(rwtemp)
                            rwtemp=''
                        no_audio=0
                        # print('dialog end,play audio:'+nlze['args'][i][j])
                    # 其余情况将字符继续拼接
                    else: 
                        rwtemp=rwtemp+str(nlze['args'][i][j])

        # 注音部分舍去注音直接拼接汉字部分
        if(start==1 and nlze['command'][i]=='ruby'):
                rwtemp=rwtemp+str(nlze['args'][i][0])
        if(no_audio==1):
            if start==1:
                if(nlze['command'][i]=='WFOUT_SHORT' or nlze['command'][i]=='end'):
                    role.append(rpn)
                    if('\\n' in rwtemp):
                        rwtemp=rwtemp.replace('\\n','\n')
                    rwlen=len(rwtemp)
                    # print('rwtemp:'+rwtemp,type(rwtemp),len(rwtemp))
                    if(rwlen>3 and '\\n' not in rwtemp[-2]):
                        rwtemp=rwtemp+'\n'
                    if(nlze['command'][i]=='end' and rwtemp==''):
                        role.pop()
                    else:
                        rolew.append(rwtemp)
                    rwtemp=''
        # 结束标识符出现时将角色名称和台词写入列表
        # if(nlze['command'][i]=='cutt_resetpause'):
        # if(nlze['command'][i]=='WFOUT_DEF'):
        #     if start==1:
        #         role.append(rpn)
        #         rwtemp=rwtemp.replace('\\n','\n')
        #         if '\n' not in rwtemp[-2]:
        #             rwtemp=rwtemp+'\n'
        #         rolew.append(rwtemp)
        #         rwtemp=''
    # print(role)
    # print(rolew)
    # print(len(rolew))
    with open(f'{export_path}/{fname}.txt','w',encoding='utf-8') as msr:
        for i in range(0,len(role)):
            if(i==0):
                msr.write(f'{oltitle}\n{oltext}')
            msr.write(f'{role[i]}:{rolew[i]}')
        print(f'File Writed:{export_path}/{fname}.txt')
    # if(fname==1000004):
    #         print(len(role),len(rolew))
    #         print(start,rpn,rwtemp)
    #         print(role,rolew)
    #         sys.exit(0)
    # print(len(role),len(rolew))