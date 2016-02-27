# -*- coding: UTF-8 -*-
import urllib
import urllib2
import cookielib
import re

#print u'\u5764'
#\u8d5e\u540c 赞同
#\u611f\u8c22 感谢
#\u63d0\u95ee 提问
#\u56de\u7b54 回答

class zhihuvote:
    def __init__(self):
        self.total = 0
        self.voters = [["name","agree","thanks","questions","answers"]]
        self.next = "/answer/13557559/voters_profile"
        self.zhihuurl = 'https://www.zhihu.com'


    def zhihulogin(self):
        self.filename = 'logincookie.txt'
        self.cookie = cookielib.MozillaCookieJar(self.filename)
        self.handler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.handler)

        
        url = self.zhihuurl + '/login/email'
        values = { 
                '_xsrf' : '60a5e9c66f694effeef9bc46c6a26c0d',
                'email' : 'mr.qile@gmail.com',
                'password' : '135797531y',
                'remember_me' : 'true'
        }
        myheader = {
                'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
                'Referer' : 'https://www.zhihu.com/'
        }

        data = urllib.urlencode(values)
        headers = myheader
        req = urllib2.Request(url,data,headers)
        response = self.opener.open(req)
        print "sucess"
        #cookie.save(ignore_discard=True, ignore_expires=True)

#    def findanswer(self):

    def checkvoters(self,next):
        url = self.zhihuurl + next
        print url
        req = urllib2.Request(url)
        response = self.opener.open(req)
        content = response.read()
        contentdecode = content.decode("utf-8")
        total = re.findall(r'"total": (.*?),',contentdecode,re.S)
        next = str(re.findall(r'"next": "(.*?)"}',contentdecode,re.S).pop())
        print next
        self.next = next
        x = re.findall(r'class=\\"zg-link\\" title=\\"(.*?)\\">.*?<span>(.*?) \\u8d5e\\u540c<.*?<span>(.*?) \\u611f\\u8c22<.*?target=\\"_blank\\">(.*?) \\u63d0\\u95ee<.*?target=\\"_blank\\">(.*?) \\u56de\\u7b54<',contentdecode,re.S)
        Items = []
        for item in x:
            Items.append([item[0].decode("unicode_escape"),item[1],item[2],item[3],item[4]])
        return Items

    def loaddata(self):
        self.zhihulogin()
        while self.next:
            partresult = self.checkvoters(self.next)
            for a in partresult:
                self.voters.append(a)
        return self.voters

#voteurl = 'https://www.zhihu.com/answer/15299264/voters_profile'

print "start"

zhihutest = zhihuvote()
result = []
result = zhihutest.loaddata()
for a in result:
    print a[0],a[1],a[2],a[3],a[4]


