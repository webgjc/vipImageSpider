#coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import json
arr=[]
k=0
req=requests.Session()
for i in range(0,8000,30):
    try:
        resp=req.get('https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E5%A5%B3%E8%A3%85+%E6%97%A0%E6%A8%A1%E7%89%B9&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word=%E5%A5%B3%E8%A3%85+%E6%97%A0%E6%A8%A1%E7%89%B9&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&pn='+str(i)+'&rn=30&gsm=1e&1507876123991=')
        resp.encoding='utf-8'
        #print(resp.text.encode('gbk','ignore'))
        #https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E5%A5%B3%E8%A3%85+%E6%97%A0%E6%A8%A1%E7%89%B9&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word=%E5%A5%B3%E8%A3%85+%E6%97%A0%E6%A8%A1%E7%89%B9&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&pn=150&rn=30&gsm=96&1507876724684=
        resjson=json.loads(resp.text)
        #print(resjson['data'][0]['fromPageTitleEnc'])
        for j in resjson['data']:
            if not j.has_key('hoverURL'):
                continue
            else:
                if j['hoverURL'] in arr:
                    continue
                else:
                    arr.append(j['hoverURL'])
                    k+=1
                    f=open('baiduimage/'+str(k).zfill(8)+'.jpg','wb')
                    img=req.get(j['hoverURL']).content
                    f.write(img)
                    f.close()
                    file=open("baiduimage.txt",'a')
                    print >> file,str(k).zfill(8)+".jpg "+j['fromPageTitleEnc']
        print "already "+str(k)
    except:
        pass