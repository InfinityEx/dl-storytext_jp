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
# 主线剧情中特殊的人物名称？
ms_spname=['SYS','ＳＹＳ','碧竜']
# print(ori_path)

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
    # fname='1000100' # 测试用

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
    # print
    rpn=''
    rwtemp=''
    rwtext=''
    senend=0
    # telop
    trpn=''
    tltitle=''
    tltemp=''
    tltext=''
    # monologue
    mono=0
    mopn=''
    monotext=''
    # outline
    oltitle=''
    oltext=''
    oltemp=''
    # 剧情概要、角色台词开始标志
    telop=0
    outline=0
    start=0
    outend=0
    teend=0
    no_audio=1
    for i in range(0,nlzelen):
        # 剧情概要处理
        if(nlze['command'][i]=='OL_TITLE' or nlze['command'][i]=='outline_title'):
            oltitle=nlze['args'][i]
            outline=1
        # 剧情概要文本拼接
        if(nlze['command'][i]=='outline'):
            # 当下一行不是ruby或者outline时合并当前的数据后关闭outline开关
                if(nlze['command'][i+1]=='outline' or nlze['command'][i+1]=='ruby'):
                    outlen=len(nlze['args'][i])
                    for a in range(0,outlen):
                        if('\\n' in nlze['args'][i][a]):
                            oltemp=str(nlze['args'][i][a])
                            oltemp=oltemp.replace('\\n','\n')
                            oltext+=oltemp
                        elif(nlze['args'][i][a]=='block_a' or nlze['args'][i][a]=='end_block'):
                            oltemp=''
                        else:
                            oltemp=str(nlze['args'][i][a])
                            oltext+=oltemp
                else:
                    outlen=len(nlze['args'][i])
                    for a in range(0,outlen):
                        if('\\n' in nlze['args'][i][a]):
                            oltemp=str(nlze['args'][i][a])
                            oltemp=oltemp.replace('\\n','\n')
                            oltext+=oltemp
                        elif(nlze['args'][i][a]=='block_a' or nlze['args'][i][a]=='end_block'):
                            oltemp=''
                        else:
                            oltemp=str(nlze['args'][i][a])
                            oltext+=oltemp
                    outline=0
                    outend=1
        if(nlze['command'][i]=='ruby'):
            if outline==1:
                # 当下一行不是ruby或者outline时合并当前的数据后关闭outline开关
                if(nlze['command'][i+1]=='outline' or nlze['command'][i+1]=='ruby'):
                    if('\\n' in nlze['args'][i][0]):
                        oltemp=str(nlze['args'][i][0])
                        oltemp=oltemp.replace('\\n','\n')
                        oltext+=oltemp
                    else:
                        oltemp=str(nlze['args'][i][0])
                        oltext+=oltemp
                else:
                    if('\\n' in nlze['args'][i][a]):
                        oltemp=str(nlze['args'][i][a])
                        oltemp=oltemp.replace('\\n','\n')
                        oltext+=oltemp
                    else:
                        oltemp=str(nlze['args'][i][a])
                        oltext+=oltemp
                    outline=0
                    outend=1
        # MONOLOGUE处理
        if nlze['args'][i]=='MONOLOGUE':
            mono=1
        if(nlze['command'][i]=='print'):
            if mono==1:
                if(nlze['command'][i+1]=='print' or 'ruby' or 'wait'):
                    moend=0
                else:
                    moend=1
                molen=len(nlze['args'][i])
                for ax in range(0,molen):
                    if str(nlze['args'][i][ax]) in ms_spname:
                        mopn=str(nlze['args'][i][ax])
                        mopn=mopn+'： '
                    elif '\\n' in nlze['args'][i][ax]:
                        motemp=str(nlze['args'][i][ax])
                        motemp=motemp.replace('\\n','\n')
                        monotext+=motemp
                if moend==1:
                    mono=0
        if(nlze['command'][i]=='ruby'):
            if mono==1:
                if(nlze['command'][i+1]=='print' or 'ruby' or 'wait'):
                    moend=0
                else:
                    moend=1
                if '\\n' in nlze['args'][i][0]:
                        motemp=str(nlze['args'][i][0])
                        motemp=motemp.replace('\\n','\n')
                        monotext+=motemp
                if moend==1:
                    mono=0
        # telop 章节背景介绍处理
        if(nlze['command'][i]=='telop'):
            telop=1
            xlen=len(nlze['args'][i])
            for x in range(0,xlen):
                tltile=tltitle+str(nlze['args'][i][x])
            tltitle+='\n'
        if(nlze['command'][i]=='print'):
            if telop==1:
                # 当下一行不是ruby或者print时合并当前的数据后关闭telop开关
                if(nlze['command'][i+1]=='print' or nlze['command'][i+1]=='ruby'):
                    tltlen=len(nlze['args'][i])
                    for b in range(0,tltlen):
                        if('\\n' in nlze['args'][i][b]):
                            tltemp=str(nlze['args'][i][b])
                            tltemp=tltemp.replace('\\n','\n')
                            tltext+=tltemp
                        elif (nlze['args'][i][b] in ms_spname):
                            trpn=nlze['args'][i][b]
                        else:
                            tltemp=str(nlze['args'][i][b])
                            tltext+=tltemp
                        telop=0
                        teend=1
        if(nlze['command'][i]=='ruby'):
            if telop==1:
                if(nlze['command'][i+1]=='print' or nlze['command'][i+1]=='ruby'):
                    if('\\n' in nlze['args'][i][0]):
                        tltemp=str(nlze['args'][i][0])
                        tltemp=tltemp.replace('\\n','\n')
                        tltext+=tltemp
                    else:
                        tltemp=str(nlze['args'][i][0])
                        tltext+=tltemp
                else:
                    if('\\n' in nlze['args'][i][0]):
                        tltemp=str(nlze['args'][i][0])
                        tltemp=tltemp.replace('\\n','\n')
                        tltext+=tltemp
                    else:
                        tltemp=str(nlze['args'][i][0])
                        tltext+=tltemp
                    telop=0
                    teend=1
        # 对话处理
        if outend+teend==2 or outend+telop==1:
            start=1
        if(nlze['command'][i]=='print'):
            if start==1:
                nxchap=nlze['command'][i+1]
                if(nxchap=='print' or nxchap=='ruby' or nxchap=='wait_print' or nxchap=='wait'):
                    senend=0
                else:
                    senend=1
                arglen=len(nlze['args'][i])
                for c in range(0,arglen):
                    # 当print内容出现了音频播放时，输出音频播放内容
                    if(str_eqrate(nlze['args'][i][c],aud_normal)>0.72):
                        no_audio=0
                        # print('dialog end,play audio:'+nlze['args'][i][j])
                    elif nlze['command'][i]=='wait':
                        rwtemp=nlze['args'][i][c]==''
                    # 当人物id包含#cn时，替换为空白
                    elif('#cn' in nlze['args'][i][c]):
                        rpn=str(nlze['args'][i][c])
                        rpn=rpn[0:rpn.rfind('#')]
                    # 当人物id包含#时，替换为空白
                    elif('#' in nlze['args'][i][c]):
                        rpn=str(nlze['args'][i][c])
                        rpn=rpn[0:rpn.rfind('#')]
                    elif(nlze['args'][i][c] in ms_spname):
                        rpn=nlze['args'][i][c]
                    # 出现{player_name}时一律替换为ユーディル
                    elif '{' in nlze['args'][i][c]:
                        rpn='ユーディル'
                    # 当人物id字母部分只有cn时，对照char_id.csv查表
                    elif 'cn' in nlze['args'][i][c] or 'dn' in nlze['args'][i][c]:
                        rpn=str(nlze['args'][i][c])
                        for d in range(0,cidlen):
                            if(rpn==cidfile['cid'][d]):
                                rpn=cidfile['jp'][d]
                    # 避免换行符出现在句子前导致文本无法正常换行
                    elif '\\n' in str(nlze['args'][i][c])[0:2]:
                        # if('#' in nlze['args'][i][c] or 'cn' in nlze['args'][i][c]):
                        #     rpn=str(nlze['args'][i][c])
                        #     rpn=rpn[0:rpn.rfind('#')]
                        # else:
                        #     if('\\n' in nlze['args'][i][c]):
                        rwtemp=str(nlze['args'][i][c])
                        rwtemp=rwtemp.replace('\\n','\n')
                        rwtext+=rwtemp
                    # 其余情况将字符继续拼接
                    else:
                        rwtext=rwtext+str(nlze['args'][i][c])
                if(senend==1):
                    rpn='\n'+rpn
                    role.append(rpn)
                    if('\\n' in rwtext):
                        rwtext=rwtext.replace('\\n','\n')
                    # rwlen=len(rwtext)
                    # print('rwtemp:'+rwtemp,type(rwtemp),len(rwtemp))
                    # if(rwlen>3 and '\\n' not in rwtext[-2]):
                    #     rwtext=rwtext+'\n'
                    rolew.append(rwtext+'\n')
                    rwtext=''
        # 注音部分舍去注音直接拼接汉字部分
        if(nlze['command'][i]=='ruby'):
            if start==1:
                nxchap=nlze['command'][i+1]
                if(nxchap=='print' or nxchap=='ruby' or nxchap=='wait_print'):
                    senend=0
                else:
                    senend=1
                if('\\n' in nlze['args'][i][0]):
                        rwtemp=str(nlze['args'][i][0])
                        rwtemp=rwtemp.replace('\\n','\n')
                        rwtext+=rwtemp
                elif nlze['command'][i]=='wait':
                        rwtemp=nlze['args'][i][c]==''
                else:
                    rwtemp=str(nlze['args'][i][0])
                    rwtext+=rwtemp
                if(senend==1):
                        rpn='\n'+rpn
                        role.append(rpn)
                        if('\\n' in rwtext):
                            rwtext=rwtext.replace('\\n','\n')
                        # rwlen=len(rwtemp)
                        # # print('rwtemp:'+rwtemp,type(rwtemp),len(rwtemp))
                        # if(rwlen>3 and '\\n' not in rwtemp[-2]):
                        #     rwtemp=rwtemp+'\n'
                        rolew.append(rwtext)
                        rwtext=''

    with open(f'{export_path}/{fname}.txt','w',encoding='utf-8') as msr:
        # write in outline
        msr.write(f'oltitle:\n{oltitle}\noltext:\n{oltext}\n')
        # write in monologue
        msr.write(f'mopn:\n{mopn}\nmotext:\n{monotext}')
        # write in telop
        msr.write(f'trpn:\n{trpn}\ntititle:\n{tltitle}\ntltext:\n{tltext}\n')
        # write in role,rolew
        for i in range(0,len(role)):
            msr.write(f'{role[i]}： {rolew[i]}')
        print(f'{oltitle}\n{oltext}\n')
        print(f'{trpn}\n{tltitle}\n{tltext}\n')
        print(f'{role}')
        print(f'{rolew}')
        print(f'File Writed:{export_path}/{fname}.txt')
    # if(fname==1000004):
    #         print(len(role),len(rolew))
    #         print(start,rpn,rwtemp)
    #         print(role,rolew)
    #         sys.exit(0)
    # print(len(role),len(rolew))