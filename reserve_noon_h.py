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


class XJTUUser(object):

    def __init__(self, config_file_path='./config.json'):
        with open(config_file_path) as config_file:
            config = json.loads(config_file.read())
        self.config = config
        self.is_login = False
        self.session = requests.Session()
        self.session.headers.update(config['headers'])
        self.session.cookies.update(config['cookies'])
    

    def login(self,weizhi):
        #--------------------------------------
        def vxpush(self,msg):
            url = 'http://wxpusher.zjiecode.com/api/send/message'
            uid = 'UID_f6KW1qbvStLZLLDAuqcnjUiIRw3Z' 
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                'Content-Type':'application/json;charset=UTF-8'
            }
            data = {
            'appToken':'AT_RL7e2VT7HZYC7YttQ8RIHvvtRrGIJdRh',
            'content': msg,
            'contentType':1,
            'uids':[uid]
            }
            print(requests.post(url,headers=headers,json=data).text)
        def check_my_seat(self):#返回你的座位字符穿
            r = self.session.get('http://rg.lib.xjtu.edu.cn:8010/my/') 
            dom = etree.HTML(r.text)
            a_text = dom.xpath('/html/body/div[2]/center/div[1]/div/div/div/div/div/div[1]/h3/text()[2]')
            jjj = dom.xpath('/html/body/div[2]/center/div[1]/div/div/div/div/div/div[2]/center/h3[1]')
            if(len(jjj)<1):
                vxpush(self,'没弄上，出现错误1')
                print('没弄上1，出现错误')
                return 0;
            if jjj[0].text == '已取消' or jjj[0].text == '已离馆' or jjj[0].text == '超时未入馆':
                vxpush(self,'没弄上，出现错误')
                print('没弄上，出现错误')
                return 0
            else:
                vxpush(self,'弄好了'+str(a_text))
                print('弄好了'+str(a_text))
                return 1    
        
        def cancel(self):
            try:
                r = self.session.get("http://rg.lib.xjtu.edu.cn:8010/my/")
                pattern = re.compile("cancelconfirm.*?'(.*?)'.*?;", re.S) 
                yu_id = re.findall(pattern, r.text)[0]
                print(yu_id)
                self.session.get("http://rg.lib.xjtu.edu.cn:8010/my/?cancel=1&ri=" + yu_id)
                #微信通知
                vxpush(self,'取消成功')
                print("取消成功")
            except Exception as e:
                print("取消失败\n" + str(e))
        #预约座位
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
            if check_my_seat(self) == 1:
                vxpush(self,'预约成功'+str(check_my_seat(self)))
                print('预约成功状态'+str(check_my_seat(self)))
                return 1
            else:
                vxpush(self,'预约失败')
                print('预约失败')
                return 0
            # if(sp == 'west3B'):
            #     r_w3=self.session.get('http://rg.lib.xjtu.edu.cn:8010/qseat?sp=west3B')
            #     s2 = json.loads(r_w3.text)['seat']
            #     if(s2[kid] == 1):
            #         return 200
            #     else:
            #         print('预约了但是没有成功,肯定是你已经预约过了')
            #         exit(0)
            #         return 0
            # if(sp == 'east3A'):
            #     r_w3=self.session.get('http://rg.lib.xjtu.edu.cn:8010/qseat?sp=east3A')
            #     s2 = json.loads(r_w3.text)['seat']
            #     if(s2[kid] == 1):
            #         return 200
            #     else:
            #         print('预约了但是没有成功，肯定是你已经预约过了')
            #         exit(0)
            #         return 0
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
        r_w3=self.session.get('http://rg.lib.xjtu.edu.cn:8010/qseat?sp=west3B')#兴庆区的，别的区得自行修改了
        r_e3=self.session.get('http://rg.lib.xjtu.edu.cn:8010/qseat?sp=east3A')
        # print(r_w3.text)
        # print('各层座位数量',end = '')
        # print(json.loads(r_e3.text)['scount'])
        s1 = json.loads(r_e3.text)['seat']
        s2 = json.loads(r_w3.text)['seat']
        # cancel(self)
        # my_list = [weizhi]
        # while (1):
        #     if check_my_seat(self) == 0:
        #         continue
        #     time.sleep(2)
        # ii=0
        # print('检测到离馆了')
        while(1):
            ii+=1
            r_new=self.session.get('http://rg.lib.xjtu.edu.cn:8010/qseat?sp=south3middle')
            s_new = json.loads(r_new.text)['seat']
            #print(s1,s2,s_new)
            print('循环次数：')
            #vxpush(self,'test')
            print(ii)
            #reserve(self,'029','south3middle')
            print("位置状态" + str(s_new[weizhi]))
            if s_new[weizhi] == 0:
                while(1):
                    if reserve(self,weizhi,'south3middle') == 1:
                        print('三楼南你的座位号是'+weizhi)
                    time.sleep(60*25)
                    cancel(self)
                        # return(0)
            time.sleep(2)

if __name__ == '__main__':
    time.sleep(60*1)#预计一分钟离馆
    weizhi = "065"
    guoguo = XJTUUser('./config.json')
    guoguo.login(weizhi)
    exit(0)
