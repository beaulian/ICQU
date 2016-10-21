# coding=utf-8
import re,signal
import requests
import urllib,urllib2,cookielib,time
import json,base64
from . import repair
from flask import Flask, request, render_template,redirect,make_response, session, jsonify
#-------------------------------------------------------------------------
header1={'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, */*',
'Referer': ' http://222.198.155.112/huxi/',
'Accept-Language': 'zh-CN',
'Content-Type': 'application/x-www-form-urlencoded',
'Accept-Encoding': 'gzip, deflate',
'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; Tablet PC 2.0; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; LCJB)',
'Host': '222.198.155.112',
'Connection': 'Keep-Alive',
'Pragma': 'no-cache'}

def resp(dict1):
    resp1 = make_response(json.dumps(dict1), 200)
    resp1.headers['Access-Control-Allow-Origin'] = '*'
    resp1.headers['Content-type']='application/json'
    return resp1
#-------------------------------------------------------------------------
def post(url, data):  
    req = urllib2.Request(url)  
    data = urllib.urlencode(data)  
    #enable cookie
    cj=cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))  
    response = opener.open(req, data)
    return cj
def handle_str(_str):
    b=_str[_str.find('" selected="selected"')-4:_str.find('" selected="selected"')]
    return b[b.find('"')+1:]
#-------------------------------------------------------------------------
def handle_body(_data):
    body_d={'op':'提交','form_build_id':'','form_token':'','form_id':'network_form',
            'xuehao':'','name':'','dianhua':'','loudong':'87','fangjian':'','chuangwei':'',
            'problem_title':'','problem_desc':'','xueyuan':'','problem_type':''}
    body_d['form_build_id']=re.findall('name="form_build_id" value="(.*?)"',_data)[0]
    body_d['form_token']=re.findall('name="form_token" value="(.*?)"',_data)[0]
    body_d['xuehao']=re.findall('name="xuehao" value="(.*?)"',_data)[0]
    body_d['name']=re.findall('name="name" value="(.*?)"',_data)[0]
    body_d['dianhua']=re.findall('name="dianhua" value="(.*?)"',_data)[0]
    body_d['xueyuan']=handle_str(_data[_data.find('xueyuan'):])
    body_d['loudong']=handle_str(_data[_data.find('loudong'):])
    body_d['fangjian']=re.findall('name="fangjian" value="(.*?)"',_data)[0]
    body_d['chuangwei']=handle_str(_data[_data.find('chuangwei'):])
    body_d['problem_type']=handle_str(_data[_data.find('problem_type'):])
    return body_d
#-------------------------------------------------------------------------
def handle_cookie(cj):
    str1=''
    for i in cj:
        str1+=i.name+'='+i.value
    return str1
        
    
@repair.route('/login',methods=['GET'])
def baoxiu():
    us=request.query_string
    us_1=us[us.find('?')+1:]
    us_2=us_1.split('||')
    username=us_2[0]
    passwd=us_2[1]
    da={'name':username,'pass':passwd,'form_build_id':'form-hBT_ElJuGEkDmEQmHVtNIUAlBbyX3Mtl53OsoFakUQ0','form_id':'user_login_block','op':'登录'}
    url1='http://222.198.155.111/huxi/node/13?destination=node/13'
    a=post(url1,da)
    if not handle_cookie(a):
        d1={'status':'0'}
        return resp(d1)
    else:
        r1=requests.get('http://222.198.155.111/huxi/network/form',cookies=a)
        d1={'content':handle_body(r1.text),'status':'200', 'cookie': handle_cookie(a)}
    return resp(d1)

@repair.route('/tijiao',methods=['POST'])
def tijiao():
    data_b={}
    x1,x2=request.form['cookie'].split('=')
    h={x1:x2}
    print h
    for i in request.form:
        if i!='cookie':
            #print request.form[i]
        	data_b[i]=request.form[i]
	#print h
    #return make_response("jajja")
    print data_b
    r2=requests.post('http://222.198.155.111/huxi/network/form',cookies=h,data=data_b)
    #print type(r2.text)
    if '不能重复报修'.decode('utf-8') in r2.text:
        print "yes"
        dict1={'status':'1','content':''}
        try:
            return resp(dict1)
        except Exception,e:
            pass
    else:
        print "no"
        cont=r2.text.encode('utf-8')
        cont=cont[cont.find('<table class='):cont.find('</table>')+8]
        dict1={'status':'200','content':cont}
        return resp(dict1)

    
    

