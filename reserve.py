#!/usr/bin/env python3
# @Author  : Guoguo
# @Blog    ：https://gwyxjtu.github.io
import os
import time
import json
import base64
import requests
from Crypto.Cipher import AES
import re
from lxml import etree
from threading import Thread

our_seat = []

class XJTUUser(object):

    def __init__(self, config_file_path='./config.json'):
        with open(config_file_path) as config_file:
            config = json.loads(config_file.read())
        self.config = config
        self.is_login = False
        self.session = requests.Session()
        self.session.headers.update(config['headers'])
        self.session.cookies.update(config['cookies'])
        #self.region = 

    def login(self):

        #--------------------------------------
        def check_my_seat(self):#返回你的座位字符穿
            r = self.session.get('http://rg.lib.xjtu.edu.cn:8086/my/')
            dom = etree.HTML(r.text)
            a_text = dom.xpath('/html/body/div[2]/center/div[1]/div/div/div/div/div/div[1]/h3/text()[2]')
            jjj = dom.xpath('/html/body/div[2]/center/div[1]/div/div/div/div/div/div[2]/center/h3[1]')
            if(len(jjj)<1):
                print('没弄上1，出现错误')
                return 0;
            if jjj[0].text == '已取消' or jjj[0].text == '已离馆' or jjj[0].text == '超时未入馆':
                print('没弄上，出现错误')
                return 0
            else:
                print('弄好了'+str(a_text))
                our_seat.append(str(a_text))
                return 1

            

        def reserve(self,kid,sp):
            r = self.session.get('http://rg.lib.xjtu.edu.cn:8086/ruguan')#入关
            #print('--------------------------')
            nn = r.text.find('<input id="csrf_token" name="csrf_token" type="hidden" value=')
            tok = r.text[nn+1+len('<input id="csrf_token" name="csrf_token" type="hidden" value='):nn+56+len('<input id="csrf_token" name="csrf_token" type="hidden" value=')]
            #print(r.text[nn+1+len('<input id="csrf_token" name="csrf_token" type="hidden" value='):nn+56+len('<input id="csrf_token" name="csrf_token" type="hidden" value=')])
            data={
            'csrf_token':tok,
            'csrf_token':tok,
            'service':'seat',
            'submit':'%E6%8F%90%E4%BA%A4',
            'rplace':'east'
            }#入关post,比较麻烦
            r = self.session.post('http://rg.lib.xjtu.edu.cn:8086/ruguan',data = data)#提交
            
            r = self.session.get('http://rg.lib.xjtu.edu.cn:8086/seat/?kid='+kid+'&sp='+sp)
            #print(r.text)
            #------------------------------新版判断
            #兴庆区的，别的区得自行修改了
            if check_my_seat(self) == 1:
                print('预约成功'+str(check_my_seat(self)))
                return 1
            else:
                print('预约失败')
                return 0

            return r.status_code
        def encrypt_pwd(raw_pwd, publicKey='0725@pwdorgopenp'):
            ''' AES-ECB encrypt '''
            publicKey = publicKey.encode('utf-8')
            # pkcs7 padding
            BS = AES.block_size
            pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
            pwd = pad(raw_pwd)
            # zero padding
            '''
            pwd = raw_pwd
            while len(raw_pwd.encode('utf-8')) % 16 != 0:
                pwd += '\0'
            '''
            cipher = AES.new(publicKey, AES.MODE_ECB)
            pwd = cipher.encrypt(pwd.encode('utf-8'))
            return str(base64.b64encode(pwd), encoding='utf-8')

        _headers = self.config['headers']
        _headers['Content-Type'] = 'application/x-www-form-urlencoded'

        # start with 302 redirection from ehall
        _r = self.session.get('http://rg.lib.xjtu.edu.cn:8086/auth/login/?next=%2Fseat%2F')

        # get cookie route
        self.session.get('https://org.xjtu.edu.cn/openplatform/login.html')

        # get JcaptchaCode and cookie JSESSIONID & sid_code
        r_JcaptchaCode = self.session.post('https://org.xjtu.edu.cn/openplatform/g/admin/getJcaptchaCode',
                              headers=_headers)

        # is_JcaptchaCode_show
        url = 'https://org.xjtu.edu.cn/openplatform/g/admin/getIsShowJcaptchaCode'
        params = {
            'userName': self.config['username'],
            '_': str(int(time.time() * 1000))
        }
        r = self.session.get(url, params=params, headers=_headers)
        print(r.text)
        # login
        url = 'https://org.xjtu.edu.cn/openplatform/g/admin/login'
        cookie = {
            'cur_appId_':'JL4oKidbLpQ='
        }
        data = {
            "loginType": 1,
            "username": self.config['username'],
            "pwd": encrypt_pwd(self.config['password']),
            "jcaptchaCode": ""
        }
        _headers['Content-Type'] = 'application/json;charset=UTF-8'
        r = self.session.post(url, data=json.dumps(data), headers=_headers,cookies=cookie)
        print(r.text)
        token = json.loads(r.text)['data']['tokenKey']

        cookie = {
            'cur_appId_':'JL4oKidbLpQ=',
            'open_Platform_User' : token
        }
        r=self.session.get('http://org.xjtu.edu.cn/openplatform/oauth/auth/getRedirectUrl?userType=1&personNo='+self.config['person_id']+'&_=1590998261976',cookies = cookie)
        print(r.text)
        r=self.session.get(json.loads(r.text)['data'])
        r=self.session.get('http://rg.lib.xjtu.edu.cn:8080/bxusr/link.jsp?uid='+self.config['username']+'&cn=%E9%83%AD%E7%8E%8B%E6%87%BF&employeeNumber='+self.config['person_id']+'&depId=%E7%94%B5%E5%AD%90%E4%B8%8E%E4%BF%A1%E6%81%AF%E5%AD%A6%E9%83%A8&mobile')#&email=867718012@qq.com去掉了
        #print(r.text)
        #---------------------登陆成功------------------------

        #print(r_w3.text)
        #print('各层座位数量',end = '')
        #print(json.loads(r_e3.text)['scount'])
        #s.update(json.loads(r_w3.text)['seat'])/seat/?kid=015&sp=north4southwest
        #print(s1,s2)


        #check_my_seat(self)
        #my_list = ['G054','G018','G005','G029','G054','G066']
        ii=0
        while(1):
            ii+=1
            r=self.session.get('http://rg.lib.xjtu.edu.cn:8086/qseat?sp='+self.config['region'])#兴庆区的，别的区得自行修改了

            #print('各层座位数量',end = '')
            s = json.loads(r.text)['seat']
            print('循环次数：')
            print(ii)

                #i = 'G054'
            if self.config['seat_id'] == '':
                for i in s:
                    if reserve(self,i,self.config['region']) == 1:
                        return(0)
                    else:
                        print('预约失败')
                        return(1)   
                continue

            if s[self.config['seat_id']] == 0:
                
                print(self.config['seat_id'])
                if reserve(self,self.config['seat_id'],self.config['region']) == 1:
                    return(0)
                else:
                    print('预约失败')
                    return(1)
                
            #s=s.pop('')
            #print(s)
            # for i in s:   
            #     if len(i)>0:
                    
            #         if i[0] == 'F' or i[0] == 'G':
            #             if s[i] == 0:
            #                 print(i)
            #                 if reserve(self,i,'north4east') == 1:
            #                     return(0)

            time.sleep(3)

if __name__ == '__main__':

    guoguo = XJTUUser('./config.json')
    dt = '2021-04-23 05:55:01'
    ts = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))

    t = int(time.time())
    cha = ts - t
    while cha >0:
        t = int(time.time())
        cha = ts - t 
        time.sleep(1)
        if(cha%10 == 0):
            print(cha)
    print("开始")
    
    #guoguo.login()
    #别的人就分别建立新的结构体就行
    #ruo = XJTUUser('./config_1.json')
    guoguo.login()
    #zxz.login()
    exit(0)
