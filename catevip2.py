#coding:utf-8
import requests
import json
import time
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')
req=requests.Session()
main=req.get("http://lady.vip.com/")
cateurl='https://category.vip.com/ajax/getCategory.php?callback=getCategory&tree_id=117'
pplist=req.get(cateurl).text
ppjson=json.loads(pplist[12:-1])
pparr=ppjson['data'][0]['children'][0]['children']
cate=0
k=0
for item in pparr:
    cate+=1
    try:
        searchurl='https://category.vip.com/'+item['url']
        sec1=req.get(searchurl)
        #f=open('test.html','w')
        #print >> f,sec1.text.encode('gbk','ignore')
        #m=re.findall(r'data-original="(.*?)" alt="(.*?)"',sec1.text)
        jsonpic=re.findall(r'list = (.*?);',sec1.text)
        piclist=json.loads(jsonpic[0])
        #print(piclist[0]['name'])
        for j in piclist:
            k+=1
            f=open('cateimage/'+str(cate)+'-'+str(k)+'.jpg','wb')
            img=req.get('http:'+j['list_img']).content
            f.write(img)
            f.close()
            file=open("catelist.txt",'a')
            print >> file,str(cate)+'-'+str(k)+".jpg "+j['name']
        pageall=re.findall(r'<span class="total-item-nums">(.*?)</span>',sec1.text)
        for i in range(2,int(pageall[0][1:-1])+1):
            nexturl=str(item['url']).replace('1.html',str(i)+'.html')
            searchurl='https://category.vip.com/'+nexturl
            sec1=req.get(searchurl)
            jsonpic=re.findall(r'list = (.*?);',sec1.text)
            piclist=json.loads(jsonpic[0])
            for j in piclist:
                k+=1
                f=open('cateimage/'+str(cate)+'-'+str(k)+'.jpg','wb')
                img=req.get('http:'+j['list_img']).content
                f.write(img)
                f.close()
                file=open("catelist.txt",'a')
                print >> file,str(cate)+'-'+str(k)+".jpg "+j['name']
            print(k)
    except:
        pass
    #print(m[23][1])