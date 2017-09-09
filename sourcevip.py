#coding:utf-8
#author:ganjiacheng
import requests
import json
import time
import re
req=requests.Session()
main=req.get("http://lady.vip.com/")
brandurl='http://lady.vip.com/index-ajax.php?act=floorBrandList&warehouse=VIP_SH&areaCode=103103&pagecode=a&preview=0&sell_time_from=&time_from=&part=today&page=1&pagesize=1352'
pplist=req.get(brandurl).text
ppjson=json.loads(pplist)
pparr=ppjson['data']['items']
j=0
for item in pparr:
    print(j)
    try:
        url='http://list.vip.com/api-ajax.php?callback=getMerchandiseIds&getPart=getMerchandiseRankList&r='+item['id']
        sec1=req.get(url)
        productList=json.loads(sec1.text[18:-1])
        products=productList['data']['getMerchandiseRankList']['products']
        for n in range(1,int(len(products)/50)+1):
            diviProduct=products[50*(n-1):n*50]
            productIds='%2C'.join(diviProduct)
            url='http://list.vip.com/api-ajax.php?callback=getMerchandiseDroplets1&getPart=getMerchandiseInfoList&productIds='+productIds+'&r='+item['id']
            res=req.get(url)
            jsonstr=json.loads(res.text[24:-1])
            imgarr=jsonstr['data']['getMerchandiseInfoList']['merchandiseInfoList']
            for i in imgarr:
                detail=req.get("http:"+i['detailUrl'])
                m=re.search(r'<div class="show-midpic ">(.*?)class="J-mer-bigImgZoom"',detail.text,re.S)
                res=m.group().replace('\n', '').replace(' ','')[32:-25]
                sourceImgurl="http:"+res
                f=open('sourceImg/'+str(j)+'.jpg','wb')
                img=req.get(sourceImgurl).content
                f.write(img)
                f.close()
                print(str(j)+".jpg "+i['productName'],file=open('sourcelist.txt','a'))
                j+=1
    except:
        pass
    time.sleep(5)