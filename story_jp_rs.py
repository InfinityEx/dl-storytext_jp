#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:时无ShiWu
#Filename:story_jp_rs.py
#Version:1.0

from operator import mod
import os
import pandas as pd
import json
import difflib
import sys


# 判断字符串相似度
def str_eqrate(str1,str2):
    return difflib.SequenceMatcher(None,str1,str2).quick_ratio()

# 剧情概要 ol_outline处理
def nor_ol_outline(n):
    i=int(n)
    otext=''
    outlen=len(nlze['args'][i])
    for a in range(0,outlen):
        if('\\n' in nlze['args'][i][a]):
            oltemp=str(nlze['args'][i][a])
            oltemp=oltemp.replace('\\n','\n')
            otext+=oltemp
        elif(nlze['args'][i][a]=='block_a' or nlze['args'][i][a]=='end_block'):
            oltemp=''
        else:
            oltemp=str(nlze['args'][i][a])
            otext+=oltemp
    return otext

# 剧情概要 ol_ruby处理
def nor_ol_ruby(n):
    i=int(n)
    otext=''
    if(nlze['command'][i]=='ruby'):
        if('\\n' in nlze['args'][i][0]):
            oltemp=str(nlze['args'][i][0])
            oltemp=oltemp.replace('\\n','\n')
            otext+=oltemp
        else:
            oltemp=str(nlze['args'][i][0])
            otext+=oltemp
    return otext

# MONOLOGUE_print处理
def nor_mo_print(n):
    i=int(n)
    mpn=''
    motext=''
    molen=len(nlze['args'][i])
    for ax in range(0,molen):
        if str(nlze['args'][i][ax]) in ms_spname:
            mpn=str(nlze['args'][i][ax])
        elif '\\n' in nlze['args'][i][ax]:
            motemp=str(nlze['args'][i][ax])
            motemp=motemp.replace('\\n','\n')
            motext+=motemp
        else:
            motemp=str(nlze['args'][i][ax])
            motext+=motemp
    return mpn,motext

# MONOLOGUE_ruby处理
def nor_mo_ruby(n):
    i=int(n)
    motext=''
    if '\\n' in nlze['args'][i][0]:
        motemp=str(nlze['args'][i][0])
        motemp=motemp.replace('\\n','\n')
        motext+=motemp
    else:
        motemp=str(nlze['args'][i][0])
        motext+=motemp
    return motext

# telop_title
def nor_te_title(n):
    i=int(n)
    tttemp=''
    xlen=len(nlze['args'][i])
    for x in range(0,xlen):
        if('\\n' in nlze['args'][i][x]):
            trctemp=str(nlze['args'][i][x])
            trctemp=trctemp.replace('\\n','\n')
            tttemp+=trctemp
        else:
            tttemp=tttemp+str(nlze['args'][i][x])
    return tttemp

# telop_print(备用)
def nor_te_print(n):
    i=int(n)
    ttrpn=''
    tptemp=''
    tltlen=len(nlze['args'][i])
    for b in range(0,tltlen):
        if('\\n' in nlze['args'][i][b]):
            txtemp=str(nlze['args'][i][b])
            txtemp=txtemp.replace('\\n','\n')
            tptemp+=txtemp
        elif (nlze['args'][i][b] in ms_spname):
            ttrpn=str(nlze['args'][i][b])
            ttrpn+='<role>'
        else:
            txtemp=str(nlze['args'][i][b])
            tptemp+=txtemp
    return ttrpn,tptemp

# telop_ruby(备用)
def nor_te_ruby(n):
    i=int(n)
    tptemp=''
    if('\\n' in nlze['args'][i][0]):
        txtemp=str(nlze['args'][i][0])
        txtemp=txtemp.replace('\\n','\n')
        tptemp+=tltemp
    else:
        txtemp=str(nlze['args'][i][0])
        tptemp+=txtemp
    return tptemp

# dialog_print
def nor_da_print(n):
    global no_audio
    global rpn
    prwtemp=''
    prwtext=''
    i=int(n)
    arglen=len(nlze['args'][i])
    for c in range(0,arglen):
        # 当print内容出现了音频播放时，输出音频播放内容
        if(str_eqrate(nlze['args'][i][c],aud_normal)>0.72):
            no_audio=0
            # print('dialog end,play audio:'+nlze['args'][i][j])
        elif nlze['command'][i]=='wait':
            prwtemp=nlze['args'][i][c]==''
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
        elif "{player_name}" in nlze['args'][i][c]:
            rpn='ユーディル'
        # 当人物id字母部分只有cn或dn时，对照char_id.csv查表
        elif 'cn' in nlze['args'][i][c] or 'dn' in nlze['args'][i][c]:
            rpn=str(nlze['args'][i][c])
            for d in range(0,cidlen):
                if(rpn==cidfile['cid'][d]):
                    rpn=cidfile['jp'][d]
        # 避免换行符出现在句子前导致文本无法正常换行
        elif '\\n' in str(nlze['args'][i][c])[0:2]:
            prwtemp=str(nlze['args'][i][c])
            prwtemp=prwtemp.replace('\\n','\n')
            prwtext+=prwtemp
        elif ' '==nlze['args'][i][c]:
            continue
        # 其余情况将字符继续拼接
        else:
            prwtemp=str(nlze['args'][i][c])
            prwtemp=prwtemp.replace('\\n','\n')
            prwtext+=prwtemp
    return prwtext

# dialog_ruby
def nor_da_ruby(n):
    i=int(n)
    prwtemp=''
    prwtxt=''
    if('\\n' in nlze['args'][i][0]):
        prwtemp=str(nlze['args'][i][0])
        prwtemp=prwtemp.replace('\\n','\n')
        prwtxt+=prwtemp
    elif nlze['command'][i]=='wait':
        prwtemp=nlze['args'][i][0]==''
    else:
        prwtemp=str(nlze['args'][i][0])
        prwtxt+=prwtemp
    return prwtxt


if __name__=='__main__':
    # 字符串定义
    aud_normal='VO_CHR_INGAMESTORY_00_00_0000'
    ori_path=os.path.split(os.path.realpath(__file__))[0]
    char_id=f'{ori_path}/char_id.csv'
    filepath=f'{ori_path}/queststory_main'
    filelist=f'{ori_path}/queststory_main.csv'
    export_path=f'{ori_path}/queststory_main_jp'
    mainstory_fnmae=''

    # 主线剧情中特殊的人物名称？
    ms_spname=['SYS','ＳＹＳ','碧竜','魔獣']
    # print(ori_path)

    # 加载charaid表
    cidfile=pd.read_csv(char_id)
    cidlen=len(cidfile['cid'])
    # 导入剧情文件列表
    eachfile=pd.read_csv(filelist)
    eflen=len(eachfile['filename'])
    # eflen=1 # 测试用
    fname=''

    # 定义剧情概要、演员角色、台词、台词暂存变量
    role=[]
    rolew=[]
    # print
    rpn=''
    rwtemp=''
    rwtext=''
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
    moend=0
    teend=0
    daend=0
    markp=0
    no_audio=1
    # startrow=0

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
        startrow=0
        
        for i in range(0,nlzelen):
            n=int(i)
            # 剧情概要处理过程：oltilte->ol outline->ol ruby
            # 剧情概要标题
            if(nlze['command'][i]=='OL_TITLE' or nlze['command'][i]=='outline_title'):
                oltitle=nlze['args'][i]
                outline=1
            
            # 剧情概要 outline
            if(nlze['command'][i]=='outline'):
                if outline==1:
                    # 当下一行不是ruby或者outline时合并当前的数据后关闭outline开关
                    if(nlze['command'][i+1]=='outline' or nlze['command'][i+1]=='ruby'):
                        start=0
                        outend=0
                    else:
                        outend=1
                    n=int(i)
                    oltemp=nor_ol_outline(n)
                    nlze['end'][i]='a'
                    oltext+=oltemp
                    if outend==1:
                        outline=0
                    else:
                        outline=1
            
            # 剧情概要 ruby
            if(nlze['command'][i]=='ruby'):
                if outline==1:
                    # 当下一行不是ruby或者outline时合并当前的数据后关闭outline开关
                    if(nlze['command'][i+1]=='outline' or nlze['command'][i+1]=='ruby'):
                        start=0
                        outend=0
                    else:
                        outend=1
                    n=int(i)
                    oltemp=nor_ol_ruby(n)
                    nlze['end'][i]='a'
                    oltext+=oltemp
                    if outend==1:
                        outline=0
                    else:
                        outline=1

            # MONOLOGUE处理
            if nlze['command'][i]=='window_type':
                if nlze['args'][i][0]=='MONOLOGUE':
                    xcmd=nlze['command'][i+1]
                    if xcmd=='print' or xcmd=='ruby':
                        mono=1
                    else:
                        moend=1
                else:
                    mono=0
                    moend=1

            # MONOLOGUE_print
            if(nlze['command'][i]=='print'):
                if mono==1:
                    ncmd=nlze['command'][i+1]
                    if(ncmd=='print' or ncmd=='ruby' or ncmd=='wait'):
                        start=0
                        moend=0
                    else:
                        moend=1
                    n=int(i)
                    mopntemp,monotemp=nor_mo_print(n)
                    nlze['end'][i]='b'
                    if mopntemp in ms_spname:
                        mopn=mopntemp+'： '
                    monotext+=monotemp
                    if moend==1:
                        mono=0
                    else:
                        mono=1

            # MONOLOGUE_ruby
            if(nlze['command'][i]=='ruby'):
                if mono==1:
                    ncmd=nlze['command'][i+1]
                    if(ncmd=='print' or ncmd=='ruby' or ncmd=='wait'):
                        start=0
                        moend=0
                    else:
                        moend=1
                    n=int(i)
                    monotemp=nor_mo_ruby(n)
                    nlze['end'][i]='b'
                    monotext+=monotemp
                    if moend==1:
                        mono=0
                    else:
                        mono=1

            # telop 章节背景介绍处理
            if(nlze['command'][i]=='telop'):
                telop=1
                tltemp=''
                n=int(i)
                ttemp=nor_te_title(n)
                tltitle=ttemp
                if nlze['command'][i+1]=='print' or nlze['command'][i+1]=='ruby':
                    teend=0
                else:
                    teend=1
                if teend==1:
                    telop=0
                else:
                    telop=1

            # telop_print(备用)
            if(nlze['command'][i]=='print'):
                if telop==1:
                    ncmd=nlze['command'][i+1]
                    if(ncmd=='print' or ncmd=='ruby' or ncmd=='wait'):
                        teend=0
                    else:
                        teend=1
                    n=int(i)
                    trp,tptem=nor_te_print(n)
                    nlze['end'][i]='c'
                    trpn=trp
                    tltext+=tptem
                    if teend==1:
                        telop=0
                    else:
                        telop=1

            # telop_ruby(备用)
            if(nlze['command'][i]=='ruby'):
                if telop==1:
                    ncmd=nlze['command'][i+1]
                    if(ncmd=='print' or ncmd=='ruby' or ncmd=='wait'):
                        teend=0
                    else:
                        teend=1
                    n=int(i)
                    tptem=nor_te_ruby(n)
                    nlze['end'][i]='c'
                    tltext+=tptem
                    if teend==1:
                        telop=0
                    else:
                        telop=1

            # 对话处理
            if 'telop' not in list(nlze['command']):
                teend=1
            if ['MONOLOGUE'] not in list(nlze['args']):
                moend=1
            if 'outline' not in list(nlze['command']):
                outend=1
            markp=moend+teend+outend
            if markp==3:
                start=1
            plst=['a','b','c']
                    
            # 对话处理 dialog
            # 对话处理 dialog_print
            if start==1 and nlze['end'][i] not in plst:
                if(nlze['command'][i]=='print'):
                    nxchap=nlze['command'][i+1]
                    if(nxchap=='print' or nxchap=='ruby' or nxchap=='wait' or nxchap=='wait_print' or nxchap=='add_book_text'):
                        daend=0
                    else:
                        daend=1
                    n=int(i)
                    rwt=nor_da_print(n)
                    if '\n' not in rpn:
                        rpn='\n'+rpn
                    rwtext+=str(rwt)
                    if daend==1:
                        start=0
                        role.append(rpn)
                        rolew.append(rwtext)
                        rwtext=''
                    else:
                        start=1
            # print(rpn,rwtext)
            # print(f'{start},{rpn},{rwtext}')

            # 对话处理 dialog_ruby        
            # 注音部分舍去注音直接拼接汉字部分
            if start==1 and nlze['end'][i] not in plst:
                if(nlze['command'][i]=='ruby'):
                    nxchap=nlze['command'][i+1]
                    if(nxchap=='print' or nxchap=='ruby' or nxchap=='wait' or nxchap=='wait_print' or nxchap=='add_book_text'):
                        daend=0
                    else:
                        daend=1
                    n=int(i)
                    rwt=nor_da_ruby(n)
                    rwtext+=str(rwt)
                    if daend==1:
                        start=0
                        role.append(rpn)
                        rolew.append(rwtext)
                        rwtext=''
                    else:
                        start=1
            
            # 对话处理 add_book_text
            if start==1 and nlze['end'][i] not in plst:
                if(nlze['command'][i]=='ruby'):
                    nxchap=nlze['command'][i+1]
                    if(nxchap=='print' or nxchap=='ruby' or nxchap=='wait' or nxchap=='wait_print' or nxchap=='add_book_text'):
                        daend=0
                    else:
                        daend=1
                    n=int(i)
                    rwt=nor_da_ruby(n)
                    rwtext+=str(rwt)
                    if daend==1:
                        start=0
                        role.append(rpn)
                        rolew.append(rwtext)
                        rwtext=''
                    else:
                        start=1

            # print(f'{start},{rpn}.repalce("\n",""),{rwtext}')

        with open(f'{export_path}/{fname}.txt','w',encoding='utf-8') as msr:
            # 调试用
            # write in outline
            msr.write(f'oltitle:\n{oltitle}\noltext:\n{oltext}\n')
            # write in monologue
            msr.write(f'mopn:\n{mopn}\nmotext:\n{monotext}\n')
            # write in telop
            msr.write(f'trpn:\n{trpn}\ntititle:\n{tltitle}\ntltext:\n{tltext}\n')

            # # 正式输出用
            # # write in outline
            # msr.write(f'{oltitle}\n{oltext}\n')
            # # write in monologue
            # msr.write(f'{mopn}\n{monotext}\n')
            # # write in telop
            # msr.write(f'{trpn}\n{tltitle}\n{tltext}\n')

            # write in role,rolew
            for i in range(0,len(role)):
                msr.write(f'\ndialog:')
                msr.write(f'{role[i]}： {rolew[i]}\n')
            # print(f'{oltitle}\n{oltext}\n')
            # print(f'{tltitle}\n{trpn}\n{tltext}\n')
            # print(f'{role}')
            # print(f'{rolew}')
            print(f'File Writed:{export_path}/{fname}.txt')
            oltitle=''
            oltext=''
            mopn=''
            monotext=''
            trpn=''
            tltitle=''
            tltext=''
            rpn=''
            rwtext=''
            role=[]
            rolew=[]
        # if(fname==1000004):
        #         print(len(role),len(rolew))
        #         print(start,rpn,rwtemp)
        #         print(role,rolew)
        #         sys.exit(0)
        # print(len(role),len(rolew))