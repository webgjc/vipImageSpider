#coding:utf-8
import requests
import dlib
import re
import cv2
import numpy as np
from PIL import Image
import io
import json
import time
import os

detector=dlib.get_frontal_face_detector()

req=requests.Session()
main=req.get("http://lady.vip.com/")
cateurl='https://category.vip.com/ajax/getCategory.php?callback=getCategory&tree_id=117'
pplist=req.get(cateurl).text
ppjson=json.loads(pplist[12:-1])
pparr=ppjson['data'][0]['children'][0]['children']
cate=0
for item in pparr:
    k=0
    cate+=1
    searchurl='https://category.vip.com/'+item['url']
    sec1=req.get(searchurl)
    if not os.path.exists('vipnomodel/'+str(cate)):
        os.mkdir("vipnomodel/"+str(cate))
    #f=open('test.html','w')
    #print >> f,sec1.text.encode('gbk','ignore')
    #m=re.findall(r'data-original="(.*?)" alt="(.*?)"',sec1.text)
    jsonpic=re.findall(r'list = (.*?);',sec1.text)
    piclist=json.loads(jsonpic[0])
    for j in piclist:
        detail=req.get('https://detail.vip.com/detail-'+str(j['brand_id'])+'-'+str(j['id'])+'.html?f=ad')
        #match=re.findall(r'data-original="(.*?)" width="420" height="531"',detail.text)
        match=re.findall(r'<a href="(.*?)" class="J-mer-bigImgZoom">',detail.text)
        for url in match:
            img=req.get('http:'+url).content
            tmpIm = io.BytesIO(img)
            image=Image.open(tmpIm)
            im = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
            if im[0].sum(1).max()-im[0].sum(1).min()<10 and im[:,0].sum(1).max()-im[:,0].sum(1).min()<10:
                dets=detector(im,0)
                if not any(enumerate(dets)):    
                    cv2.imwrite('vipnomodel/'+str(cate)+'/'+str(cate)+'-'+str(k).zfill(8)+".jpg",im)
                    print(str(cate)+'-'+str(k).zfill(8)+".jpg "+j['name'],file=open("vipnomodel.txt",'a'))
                    k+=1
    pageall=re.findall(r'<span class="total-item-nums">(.*?)</span>',sec1.text)
    for i in range(2,int(pageall[0][1:-1])+1):
        nexturl=str(item['url']).replace('1.html',str(i)+'.html')
        searchurl='https://category.vip.com/'+nexturl
        sec1=req.get(searchurl)
        jsonpic=re.findall(r'list = (.*?);',sec1.text)
        piclist=json.loads(jsonpic[0])
        for j in piclist:
            detail=req.get('https://detail.vip.com/detail-'+str(j['brand_id'])+'-'+str(j['id'])+'.html?f=ad')
            match=re.findall(r'<a href="(.*?)" class="J-mer-bigImgZoom">',detail.text)
            for url in match:
                img=req.get('http:'+url).content
                tmpIm = io.BytesIO(img)
                image=Image.open(tmpIm)
                im = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
                if im[0].sum(1).max()-im[0].sum(1).min()<10 and im[:,0].sum(1).max()-im[:,0].sum(1).min()<10:
                    dets=detector(im,0)
                    if not any(enumerate(dets)):    
                        cv2.imwrite('vipnomodel/'+str(cate)+'/'+str(cate)+'-'+str(k).zfill(8)+".jpg",im)
                        print(str(cate)+'-'+str(k).zfill(8)+".jpg "+j['name'],file=open("vipnomodel.txt",'a'))
                        k+=1
        print(k)