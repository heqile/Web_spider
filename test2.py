import urllib2
import urllib
import re
import thread
import time


class Spider_model:
    def __init__(self):
        self.page = 1
        self.pages = []
        self.enable = False

    def getpage(self,page):
        myUrl = "http://www.qiushibaike.com/textnew/page" + page
        my_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0'
        myHeader = {'User-Agent' : my_agent}
        req = urllib2.Request(myUrl,headers=myHeader)
        response = urllib2.urlopen(req)
        myPage = response.read()

        unicodePage = myPage.decode("utf-8")
        #filename = 'testpyt.html'
        #f = open(filename,'w+')
        #f.write(myPage)
        #f.close()

        myItems = re.findall('<div.*?class="content">(.*?)<!--',unicodePage,re.S)
        Items = []
        for a in myItems:
            Items.append(a.replace("<br/>","\n"))
        return Items

    def loadpage(self):
        while self.enable:
            if len(self.pages) < 2:
                try:
                    mypage = self.getpage(str(self.page))
                    self.pages.append(mypage)
                    self.page += 1
                except:
                    print 'could not connect!'
            else:
                time.sleep(1)

    def showpage(self,nowpage,page):
        for item in nowpage:
            print item
            print u'page %d' %page
            myInput = raw_input()
            if myInput == "quit":
                self.enable = False
                break

    def start(self):
        self.enable = True
        page = self.page

        print u'Now Loading...'
        
        thread.start_new_thread(self.loadpage,())

        while self.enable == True:
            if self.pages:
                nowpage = self.pages[0]
                del self.pages[0]
                self.showpage(nowpage,page)
                page += 1


print u'press Entre to read messages: '
print u"enter 'quit' to exit"
raw_input(' ')
myModel = Spider_model()
myModel.start()



