#coding:utf-8
#author:ganjiacheng
import requests
import json
import time
req=requests.Session()
main=req.get("http://lady.vip.com/")
brandurl='http://lady.vip.com/ajax/getBrandRank.php?part=selling&warehouse=VIP_SH&areaCode=103103&pagecode=a&brandInfoExt%5Bfields%5D=displayEndtime%2CsalesNo%2CbrandImage%2CmobileImageOne%2Cagio%2CsalesName%2CbrandStoreSn%2CvendorSaleMessage%2CisSpecialBanner%2ChiddenEndTime%2CiconInfo%2Clink&brandInfoExt%5BstartIndex%5D=0&brandInfoExt%5Bnum%5D=36&preview=0&sell_time_from=&time_from=&_=1507814732260'
pplist=req.get(brandurl).text
ppjson=json.loads(pplist)
pparr=ppjson['data']['items']
listfile=open("list.txt",'a')
j=0
for item in pparr:
    print(j)
    try:
        url='http://list.vip.com/api-ajax.php?callback=getMerchandiseIds&getPart=getMerchandiseRankList&r='+str(item)
        sec1=req.get(url)
        productList=json.loads(sec1.text[18:-1])
        products=productList['data']['getMerchandiseRankList']['products']
        for n in range(1,int(len(products)/50)+1):
            diviProduct=products[50*(n-1):n*50]
            productIds='%2C'.join(diviProduct)
            url='http://list.vip.com/api-ajax.php?callback=getMerchandiseDroplets1&getPart=getMerchandiseInfoList&productIds='+productIds+'&r='+str(item)
            res=req.get(url)
            jsonstr=json.loads(res.text[24:-1])
            imgarr=jsonstr['data']['getMerchandiseInfoList']['merchandiseInfoList']
            for i in imgarr:
                smallImgurl=i['smallImage']
                sourceImgurl="http:"+smallImgurl
                f=open('images/'+str(j)+'.jpg','wb')
                img=req.get(sourceImgurl).content
                f.write(img)
                f.close()
                print(str(j)+".jpg "+i['productName'],file=open("list.txt",'a'))
                j+=1
    except:
        pass
    time.sleep(5)