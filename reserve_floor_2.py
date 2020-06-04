#!/usr/bin/env python3
# @Author  : Guoguo
# @FileName: morning.py
# @Blog    ：https://gwyxjtu.github.io
import os
import time
import json
import base64
import requests
from Crypto.Cipher import AES
import re

class XJTUUser(object):

    def __init__(self, config_file_path='./config.json'):
        with open(config_file_path) as config_file:
            config = json.loads(config_file.read())
        self.config = config
        self.is_login = False
        self.session = requests.Session()
        self.session.headers.update(config['headers'])
        self.session.cookies.update(config['cookies'])

    def login(self):
        def reserve(self,kid,sp):
            r = self.session.get('http://rg.lib.xjtu.edu.cn:8010/ruguan')#入关
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
            r = self.session.post('http://rg.lib.xjtu.edu.cn:8010/ruguan',data = data)#提交
            
            r = self.session.get('http://rg.lib.xjtu.edu.cn:8010/seat/?kid='+kid+'&sp='+sp)
            #print(r.text)
            #------------------------------新版判断
            #兴庆区的，别的区得自行修改了
            if(sp == 'west3B'):
                r_w3=self.session.get('http://rg.lib.xjtu.edu.cn:8010/qseat?sp=west3B')
                s2 = json.loads(r_w3.text)['seat']
                if(s2[kid] == 1):
                    return 200
                else:
                    print('预约了但是没有成功,肯定是你已经预约过了')
                    exit(0)
                    return 0
            if(sp == 'east3A'):
                r_w3=self.session.get('http://rg.lib.xjtu.edu.cn:8010/qseat?sp=east3A')
                s2 = json.loads(r_w3.text)['seat']
                if(s2[kid] == 1):
                    return 200
                else:
                    print('预约了但是没有成功，肯定是你已经预约过了')
                    exit(0)
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
        _r = self.session.get('http://rg.lib.xjtu.edu.cn:8010/auth/login/?next=%2Fseat%2F')

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
        r_s2=self.session.get('http://rg.lib.xjtu.edu.cn:8010/qseat?sp=south2')#兴庆区的，别的区得自行修改了
        r_n2=self.session.get('http://rg.lib.xjtu.edu.cn:8010/qseat?sp=north2elian')
        #print(r_w3.text)
        #print('各层座位数量',end = '')
        #print(json.loads(r_e3.text)['scount'])
        s1 = json.loads(r_s2.text)['seat']
        s2 = json.loads(r_n2.text)['seat']
        #s.update(json.loads(r_w3.text)['seat'])/seat/?kid=015&sp=north4southwest
        print(s1,s2)



        #my_list = ['X115','X117','X113','X109','X111']
        #reserve(self,'X155','east3A')
        while(1):
            r_s2=self.session.get('http://rg.lib.xjtu.edu.cn:8010/qseat?sp=south2')#兴庆区的，别的区得自行修改了
            r_n2=self.session.get('http://rg.lib.xjtu.edu.cn:8010/qseat?sp=north2elian')
            #print(r_w3.text)
            #print('各层座位数量',end = '')
            #print(json.loads(r_e3.text)['scount'])
            s1 = json.loads(r_s2.text)['seat']
            s2 = json.loads(r_n2.text)['seat']
            print(s1,s2)
            # for i in my_list:
            #     if s1[i] == 0:
            #         print(i)
            #         if reserve(self,i,'east3A') == 200:
            #             print('三楼东侧侧你的座位号是'+i)
            #             exit(0)
            for i in s1:
                if s1[i] == 0:
                    print(i)
                    if reserve(self,i,'south2') == 200:
                        print('二楼南侧'+i)
                        exit(0)
            for i in s2:
                if s2[i] == 0:
                    print(i)
                    if reserve(self,i,'north2elian') == 200:
                        print('而楼北侧'+i)
                        exit(0)
            time.sleep(2)


if __name__ == '__main__':
    #print('begin')
    #time.sleep(18600)
    guoguo = XJTUUser()
    guoguo.login()
