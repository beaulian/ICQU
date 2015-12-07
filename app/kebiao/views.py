# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, request, render_template,redirect,make_response
import json
from json import *
import hashlib
global wdata
from . import kebiao

wdata=[[['' for i in range(5)]for i in range(7)]for i in range(19)]

def hmd5(str1):
    m = hashlib.md5()  
    m.update(str1)
    return m.hexdigest()


def handle0(_data):
    m=_data
    f='节'.decode('utf-8')
    x=m.find(f)
    data=m[x:]
    data=data.split('序号'.decode('utf-8'))
    data[1]=data[1][data[1].find(f):]
    soup=BeautifulSoup(data[0],from_encoding='utf-8')
    x=soup("td")
    d={'课程':[],'任课老师':[],'时间':[],'地点':[],'周次':[]}
    for i in range(len(x)):
        if i%13==1:
            d['课程'].append(x[i].text.encode('utf-8'))
        if i%13==9:
            d['任课老师'].append(x[i].text.encode('utf-8'))
        if i%13==10:
            d['周次'].append(x[i].text)
        if i%13==11:
            d['时间'].append(x[i].text)
        if i%13==12:
            d['地点'].append(x[i].text.encode('utf-8')) 
    soup=BeautifulSoup(data[1],from_encoding='utf-8')
    x=soup("td")
    for i in range(len(x)):
        if i%12==1:
            d['课程'].append(x[i].text.encode('utf-8'))
        if i%12==7:
            d['任课老师'].append(x[i].text.encode('utf-8'))
        if i%12==9:
            d['周次'].append(x[i].text)
        if i%12==10:
            d['时间'].append(x[i].text)
        if i%12==11:
            d['地点'].append(x[i].text.encode('utf-8')) 

    return d

def trans(_a):
    if _a==u'\u4e00':
        return 1
    if _a==u'\u4e8c':
        return 2
    if _a==u'\u4e09':
        return 3
    if _a==u'\u56db':
        return 4
    if _a==u'\u4e94':
        return 5
    if _a==u'\u516d':
        return 6
    if _a==u'\u65e5':
        return 7
    else:
        return 0

def handle1(_d):
    global te
    t=[]
    for i in _d['时间']:
        x=i.find(u'节')
        i=[trans(i[0]),i[2].encode('utf-8'),i[4:x].encode('utf-8')]

        t.append(i)
        
    for i in range(0,len(_d['任课老师'])):
        if _d['任课老师'][i]=='':
            _d['任课老师'][i]=_d['任课老师'][i-1]
    _d['时间']=t

    k=[]
    for i in range(0,len(_d['课程'])):
        
        if _d['课程'][i]=='':
            k.append(k[i-1])
        else:
            x=_d['课程'][i].find(']')
            h=_d['课程'][i][x+1:]
            k.append(h)
    _d['课程']=k

        
    r=[]
    for i in _d['周次']:
        m=[0]*20
        if'-'not in i and','not in i:
            m[int(i)-1]=1
            r.append(m)
            continue
        t=re.findall('\d+-\d+',i)
        for j in t:
            x=j.split('-')
            a=int(x[0])
            b=int(x[1])
            for k in range(a,b+1):
                m[k-1]=1
        
        if ',' in i:
            i=i.split(',')
            for j in i:
                if'-' not in j:
                    m[int(j)-1]=1
        r.append(m)
    _d['周次']=r           
    return _d

def handle2():
    for i in range(len(data['任课老师'])):
        for h in range(19):
            if data['周次'][i][h]:
                wdata[h][int(data['时间'][i][0])-1][(int(data['时间'][i][1])+1)/ 2-1] = data['课程'][i] + " "+data['地点'][i]+" "+data['任课老师'][i]
                   
    
@kebiao.route('/form',methods=['GET'])
def _form():
    global wdata
#if __name__=='__main__':
    us=request.query_string
    us_1=us[us.find('?')+1:]
    us_2=us_1.split('||')
    username=us_2[0]
    passwd=us_2[1]
    global data
    #username='20144479'
    #passwd='myself19951028'
    agu=hmd5(username+hmd5(passwd)[:30].upper()+'10611')[:30].upper()
    d1={'txt_dsdsdsdjkjkjc':username,'txt_dsdfdfgfouyy':passwd,'Sel_Type':'STU','__VIEWSTATEGENERATOR':'CAA0A5A7','efdfdfuuyyuuckjg':agu}
    r1=requests.post('http://202.202.1.176:8080/_data/index_login.aspx',data=d1)
    a=r1.cookies
    d2={'Sel_XNXQ':20150,'rad':'on','px':1}
    r2=requests.post('http://202.202.1.176:8080/znpk/Pri_StuSel_rpt.aspx',data=d2,cookies=a)
    _data=r2.text
    data=handle0(_data)
    data=handle1(data)
    handle2()
    test=json.dumps(wdata)
    wdata=[[['' for i in range(5)]for i in range(7)]for i in range(19)]
    resp = make_response(test, 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-type']='application/json'
    return resp

