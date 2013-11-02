#!/usr/bin/python
import urllib2,sys,sqlite3,re
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def  __init__(self):
        HTMLParser.__init__(self)
        self.t=False
        self.trans=[]
        self.prs=[]
        self.pr=False
    def handle_starttag(self, tag, attrs):
        if tag=='div':
            for attr in attrs:
                if attr==('class','hd_prUS') or \
                 attr==('class','hd_pr'):
                    self.pr=True
        if tag=='span':                       
            for attr in attrs:
                if attr==('class','def'):
                    self.t=True
    def handle_data(self, data):
        if self.t:
            if data!='(=':
                num=str(len(self.trans)+1)
                self.trans.append(num+'. '+data)
            self.t=False
        if self.pr:
            self.prs.append(data)
            self.pr=False
    def getTrans(self):
        return self.trans
    def getPr(self):
        return self.prs
class trans:
    _URL='http://cn.bing.com/dict/search'
    _DBPATH='./dic.sqlite'
    def __init__(self):
        self.url=trans._URL+"?q=%s&go=&qs=bs&form=CM&mkt=zh-CN&setlang=ZH"
        self.html=None
        self.sjoin=None
        self.pr=None
        self.word=None
        self.conn=sqlite3.connect(trans._DBPATH)
        self.cur = self.conn.cursor()
    def getHtml(self):
        self.url=self.url %self.word
        req = urllib2.Request(self.url)
        fd=urllib2.urlopen(req)
        self.html=fd.read()
        self.html=unicode(self.html,'utf-8')
        fd.close()
    
    def parseHtml(self,flag='qt'):
        self.qt=flag
        parser = MyHTMLParser()
        self.html=parser.unescape(self.html)
        parser.feed(self.html)
        s=parser.getTrans()
        self.pr=parser.getPr()
        
        if s==[]:
            self.sjoin=''
        else:
            if self.qt=='qt':
                self.sjoin='<br>'.join(s)
            else:
                self.sjoin='\n'.join(s)
        if len(self.pr)==2:
            tmp = self.pr[0]+','+self.pr[1]
            return tmp,self.sjoin
        else:
            return '',self.sjoin

    def saveDB(self):
        
        if len(self.pr)==2:
            uspr=self.pr[0]
            ukpr=self.pr[1]
        else:
            uspr=''
            ukpr=''
        if self.sjoin!='':
            self.cur.execute("insert into translate values(\'%s\',\'%s\',\'%s\',\'%s\');" \
                        %(self.word,uspr,ukpr,self.sjoin))
            self.conn.commit()

    def isExists(self,word,action=None):
        self.word=word
        if action=='del':
            self.cur.execute("delete from translate where word=\'%s\'" %self.word)
        rows=self.cur.execute("select * from translate where word=\'%s\'" %self.word)
        key=rows.fetchall()

        if key==[]:
            return None
        else:
            return key
    def closeDB(self):
        self.conn.close()
class Fecth:
    def __init__(self):
        self.t=trans()    
        self.rows=None
        self.zh=None
    def searchDB(self,lis,action):
        g=re.match('[a-zA-Z]+',lis)
        if g:
            self.rows=self.t.isExists(lis,action)
            return self.rows
        return 1
    def fecth(self,flag):
        #print 'Net fetching...'
        self.t.getHtml()
        self.zh=self.t.parseHtml(flag)
        self.t.saveDB()
        
        return self.zh
    def close(self):
        self.t.closeDB()
      

if __name__=='__main__':
    action=None
    f=Fecth()

    if len(sys.argv)< 2:
        sys.exit(1)
    if len(sys.argv)==3:
        action=sys.argv[2]
    s=sys.argv[1]
    rows=f.searchDB(s,action) 

    if rows:
        if rows==1:
            sys.exit(1)
        for row in rows:
            print row[0]
            if row[1]!='':
                print row[1],',',row[2]
            print row[3]
    else:
        zh=f.fecth('qt')
        print zh[0]
        print zh[1]
    f.close()