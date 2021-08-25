# -*- coding:utf-8 -*-
"""
图片任意拼接，参数化形式代码
使用指南：
    1. 修改常量的数值，可以实现不同样子的图片拼接，例如拼接成5*20，或者100*200的大图，每张小图也可以控制大小
    2. 可以自定义函数让图片不仅仅是全部拼接成一张图，也可以自定义哪些图进行拼接。
"""
from PIL import Image
import os
import json
from requests.adapters import HTTPAdapter
import requests
import random
import GoogleZXY2pt as coord


IMAGE_SIZE = 256  # 图片大小
IMAGE_SIZE2 = 512

POIBeginId = 1600000000 #1573550006
POIBeginId_bak = 1600000000

#######################################
#将下载下来的2级图片，分别合并成天空盒的六个面
#######################################
def image_Merge_by_folder(srcDir, outDir):
    IMAGE_COLUMN =4
    IMAGE_ROW = 4
    print('IMAGE_COLUMN = {},IMAGE_ROW = {}....'.format(IMAGE_COLUMN, IMAGE_ROW))
    #front
    x=0
    y=0
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE2, IMAGE_ROW * IMAGE_SIZE2))
    savetemppath = outDir +'2_f.jpg'
    if not os.path.exists(savetemppath):
        for y_index in range(0,4):
            for x_index in range(0,4):
                filename = '2_'+str(y_index)+'_'+str(x_index)+'.jpg'
                fromfilepath = srcDir + filename
                if os.path.exists(fromfilepath): 
                    from_image = Image.open(fromfilepath).resize((IMAGE_SIZE2, IMAGE_SIZE2), Image.ANTIALIAS)
                    to_image.paste(from_image, (x*IMAGE_SIZE2, y*IMAGE_SIZE2))
                x = x +1
                if x==4:
                    y = y+1
                    x = 0
                print('front: x={},  y={}'.format(x,y))
        success = to_image.save(savetemppath)
    #right
    x=0
    y=0
    savetemppath = outDir +'2_r.jpg'
    if not os.path.exists(savetemppath):
        for y_index in range(0,4): 
            for x_index in range(4,8):
                filename = '2_'+str(y_index)+'_'+str(x_index)+'.jpg'
                fromfilepath = srcDir + filename
                if os.path.exists(fromfilepath): 
                    from_image = Image.open(fromfilepath).resize((IMAGE_SIZE2, IMAGE_SIZE2), Image.ANTIALIAS)
                    to_image.paste(from_image, (x*IMAGE_SIZE2, y*IMAGE_SIZE2))
                x = x +1
                if x==4:
                    y = y+1
                    x = 0
                print('front: x={},  y={}'.format(x,y))
        success = to_image.save(savetemppath)
    #backend
    x=0
    y=0
    savetemppath = outDir +'2_b.jpg'
    if not os.path.exists(savetemppath):
        for y_index in range(0,4): 
            for x_index in range(8,12):
                filename = '2_'+str(y_index)+'_'+str(x_index)+'.jpg'
                fromfilepath = srcDir + filename
                if os.path.exists(fromfilepath): 
                    from_image = Image.open(fromfilepath).resize((IMAGE_SIZE2, IMAGE_SIZE2), Image.ANTIALIAS)
                    to_image.paste(from_image, (x*IMAGE_SIZE2, y*IMAGE_SIZE2))
                x = x +1
                if x==4:
                    y = y+1
                    x = 0
                print('front: x={},  y={}'.format(x,y))
        success = to_image.save(savetemppath)
    #left
    x=0
    y=0
    savetemppath = outDir +'2_l.jpg'
    if not os.path.exists(savetemppath):
        for y_index in range(0,4): 
            for x_index in range(12,16):
                filename = '2_'+str(y_index)+'_'+str(x_index)+'.jpg'
                fromfilepath = srcDir + filename
                if os.path.exists(fromfilepath):
                    from_image = Image.open(fromfilepath).resize((IMAGE_SIZE2, IMAGE_SIZE2), Image.ANTIALIAS)
                    to_image.paste(from_image, (x*IMAGE_SIZE2, y*IMAGE_SIZE2))
                x = x +1
                if x==4:
                    y = y+1
                    x = 0
                print('front: x={},  y={}'.format(x,y))
        success = to_image.save(savetemppath)
    #top
    x=0
    y=0
    savetemppath = outDir +'2_u.jpg'
    if not os.path.exists(savetemppath):
        for y_index in range(0,4): 
            for x_index in range(16,20):
                filename = '2_'+str(y_index)+'_'+str(x_index)+'.jpg'
                fromfilepath = srcDir + filename
                if os.path.exists(fromfilepath):
                    from_image = Image.open(fromfilepath).resize((IMAGE_SIZE2, IMAGE_SIZE2), Image.ANTIALIAS)
                    to_image.paste(from_image, (x*IMAGE_SIZE2, y*IMAGE_SIZE2))
                x = x +1
                if x==4:
                    y = y+1
                    x = 0
                print('front: x={},  y={}'.format(x,y))
        success = to_image.save(savetemppath)
     #down
    x=0
    y=0
    savetemppath = outDir +'2_d.jpg'
    if not os.path.exists(savetemppath):
        for y_index in range(0,4): 
            for x_index in range(20,24):
                filename = '2_'+str(y_index)+'_'+str(x_index)+'.jpg'
                fromfilepath = srcDir + filename
                if os.path.exists(fromfilepath):
                    from_image = Image.open(fromfilepath).resize((IMAGE_SIZE2, IMAGE_SIZE2), Image.ANTIALIAS)
                    to_image.paste(from_image, (x*IMAGE_SIZE2, y*IMAGE_SIZE2))
                x = x +1
                if x==4:
                    y = y+1
                    x = 0
                print('front: x={},  y={}'.format(x,y))
        success = to_image.save(savetemppath)
        print('merge pictures success = {}....'.format(savetemppath))
    
#######################################
#将下载URL图片，并保存到saveDir
#######################################
def download_img(img_url, saveDir):
    print (img_url)
    r = requests.get(img_url, stream=True)
    print(r.status_code) # 返回状态码
    if r.status_code == 200:
        open(saveDir, 'wb').write(r.content) # 将内容写入图片
        print("done")
    del r

#######################################
#将下载URL中poi的信息，创建poi，guide，720，720 search 详情，并下载poi图片，保存到savedir
#######################################
def downloadPOIInfo(urlInfo,saveDir,id,dictPOIInfo,dictGuide,dict720poi,dict720guide,dict720search,dict720Model,lenoftour):
    if len(urlInfo)<1:
        return
    #create folder:
    saveDirPOI = saveDir + 'poi/'
    if not os.path.exists(saveDirPOI):
        os.mkdir(saveDirPOI)
    saveDirPOI_image = saveDirPOI + 'image/'
    if not os.path.exists(saveDirPOI_image):
        os.mkdir(saveDirPOI_image)
    #set up http request
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    try:
        data = s.get(urlInfo, timeout=50)
        res = data.text
    except requests.exceptions.RequestException as e:
        data = s.get(urlInfo, timeout=50)
        res =  data.text
    #get information from responses
    if data.status_code == 200:
        print('downloadPOIInfo...' + urlInfo)
        #print(res)
        result = json.loads(res)
        code = result['code']
        if code == '0' and 'data' in result.keys():
            id +=1
            data = result['data']
            ##
            name = data.get('name')
            longlat = data.get('lnglat')
            address = data.get('address')
            x,y = coord.LatLonToMeters(longlat[1],longlat[0])
            #POI/poi.txt：
            #id =  ? | originalId =0 | adminId =3 | provinceId =2 | countryId =1 | language =4 | population = 12000000| groupValue = ?| lon =  | lat =  | x =  | y =  | price = 0.0 | currencyUnit = USD | recomType = 15241 | type = 100 | subType = 15241 | brandType = 0 | subbrand = 0 | layer = 1 | name =  | nameZH  = | nameEN = '' | namePY = '' | nameFR = '' | address =  |addressZH ='' | addressEN = '' | addressPY ='' | addressFR  = ''| phone = '' | adminName = '北京市' | adminNameZH = '北京市'| adminNameEN  =‘’| adminNamePY  = ‘’| adminNameFR = ‘’ | adminPostCode = ‘’
            poiinfo = '{}|0|3|2|1|4|12000000|0|{}|{}|{}|{}|0.0|USD|15241|100|15241|0|0|1|{}|{}| | | |{}|{}| | | | |北京市｜北京市｜Beijing｜Beijing｜Beijing｜ '.format(id,longlat[0],longlat[1],x,y,name,name,address,address)
            dictPOIInfo.append(poiinfo)

            ##get poi descreiption and download image
            intro = data.get('intro')
            #thumbnail: "//view.luna.vizen.cn/release/pic/poi/58258a40888f907f4fd63b14/20161211230137_03805.jpg"
            thumbimage = 'https:' + data.get('thumbnail')
            image_path = saveDirPOI_image + '\{}.jpg'.format(id)
            download_img(thumbimage,image_path)
            #http://view.luna.vizen.cn/release/audio/poi/58258a40888f907f4fd63b14/20170103164005_02267.mp3"
            #audioIntro = data.get('audioIntro') #mp3

            #guideinfo/guide.txt：
            reviewnumber=random.randint(100,500)
            photoId = id
            photoPath = 'JPG/T/80000_gugong/T/'
            #https://jpartner.erlinyou.com/JPG/T/1/T/2310201.jpg
            randomTime = '2021-05-03 12:00:00'
            photoArr = ' '
            #id =  | adminId = 3 | provinceId = 2 | linkPoiId = poiId | lon =  | lat =  | type = 10 | photoSave = ? | cuisine = 0 | star  = 5| language = 4 | like =random.randint(500,1000)| dislike = random.randint(1,50) | partnerId = 0 | reviewNumber = random.randint(100,500)| 5StarRN = random.randint(200,300) | 4StarRN = random.randint(100,200) | 3StarRN = random.randint(0,100) | 2StarRN = random.randint(1,10)| ownerId =0 | readNumber = reviewNumber + random.randint(1,1000) | rank= random.randint(3.0,5.0) | photoNumber = random.randint(1,10) | mainPhoto= ?| photoPath =  'JPG/T/gugong/T/'| publishDate = randomTime | photoArr = 1111,2222,3333 | website = '' | email = '' | hotelId = '' | expediaId = '' | openTime = '' ########| descripton = '' | summary | TTS
            #<descripton><Html><HEAD><style>a:link {color:#00aeea;text-decoration:none;}h1,h2,h3,h4,h5{font-size:18px} h6{font-size:16px} body{font-size:16px}
            #</style></HEAD><BODY>
            #<h4> 八水河 </h4>
            # <p> 沿崂山南部公路前行约10公里，就到达八水河。八水河是以八条漳水汇集成一条不长的山涧而得名。 </p> 
            # <p> <img src = "1573520000.jpg"/> </p> 
            #</BODY>
            #</Html>
            #</descripton>
            #<summary>沿崂山南部公路前行约10公里，就到达八水河。八水河是以八条漳水汇集成一条不长的山涧而得名。</summary>
            #<TTS>沿崂山南部公路前行约10公里，就到达八水河。八水河是以八条漳水汇集成一条不长的山涧而得名。</TTS>
            guideInfo = '{}|3|2|{}|{}|{}|10|1|0|5|4|{}|{}|0|{}|{}|{}|{}|{}|0|{}|4.8|{}|{}|{}|{}|{}| | | | | '.format(id,id,longlat[0],longlat[1],random.randint(500,1000),random.randint(1,50),reviewnumber,reviewnumber-random.randint(50,100),random.randint(10,50),random.randint(5,10),random.randint(0,10),reviewnumber+random.randint(100,500),random.randint(1,10),photoId,photoPath,randomTime,photoArr)
            description_head = '''<descripton>
                <Html>
                <HEAD>
                <style>
                h1,h2,h3,h4,h5{font-size:18px} h6{font-size:16px} body{font-size:16px}
                </style>
                </HEAD>
                <BODY>'''
            description_end = '''</BODY>
                </Html>
                </descripton>'''
            description = '<h4> {} </h4>'.format(name) + '<p> {} </p> '.format(intro) + '<p> <img src = "{}.jpg"/> </p>'.format(id)
            guideInfo += description_head + description + description_end
            summary = '<summary> {} </summary>'.format(intro)
            tts = '<TTS> {} </TTS>'.format(intro)
            guideInfo += summary + tts
            dictGuide.append(guideInfo)
            ## write 720/hpoi/hpoi.txt:
            #id =?| originalId =0| adminId =3| provinceId =2| countryId =1| language=4 | population = 0| groupValue =0| lon = ? | lat = ? | x = ? | y = ? | price = 0.0 | currencyUnit = USD | recomType =15241| type = 100| subType =15241 | brandType=0 | subbrand=0 | layer=1 | name =?| nameZH =?| nameEN =''| namePY ='' | nameFR ='' | address= ? |addressZH =?| addressEN='' | addressPY='' | addressFR='' | phone='' | adminName='北京市' | adminNameZH=‘北京市’ | adminNameEN =‘’ | adminNamePY =‘’ | adminNameFR =‘’ | adminPostCode =‘’
            the720info = '{}|0|3|2|1|4|0|0|{}|{}|{}|{}|0.0|USD|15241|100|15241|0|0|1|{}|{}| | | |{}|{}| | | | |北京市｜北京市｜Beijing｜Beijing｜Beijing｜ '.format(id,longlat[0],longlat[1],x,y,name,name,address,address)
            dict720poi.append(the720info)

            # write 720/hguide/hguide.txt:
            #id =?| adminId =3| provinceId=2 | linkPoiId=hpoiId | lon = ? | lat = ? | type =10 | photoSave =0 | cuisine = 0 | star = 0 | language =4| like =0 | dislike=0 | partnerId=0 | reviewNumber = random.randint(200,1000) | 5StarRN  = reviewNumber-100| 4StarRN = random.randint(1,50) | 3StarRN = random.randint(1,10) | 2StarRN = random.randint(1,10)| ownerId = 0 | readNumber = reviewNumber + random.randint(100,500) | rank = random.randint(1.0,5.0) | photoNumber=1 | mainPhoto= ? | photoPath = https://partner1.jingcailvtu.org/WEBP/Shijingtu | publishDate = 2021-05-05 12:00:00 | photoArr = | website ='' | email ='' | hotelId ='' | expediaId ='' | openTime ='' ######| descripton  | summary | TTS
            #<descripton>
            #白居易草堂位于江西庐山风景区花径公园内，1988年在园中建有“白居易草堂陈列室”，1996年著名雕塑家王克庆制作的白居易石像立于湖畔。
            #</descripton>
            #<summary>
            #白居易草堂位于江西庐山风景区花径公园内，1988年在园中建有“白居易草堂陈列室”，1996年著名雕塑家王克庆制作的白居易石像立于湖畔。
            #</summary>
            #<TTS>

            photoPath = 'JPG/Shijingtu/80000_gugong/T/'
            #https://jpartner.erlinyou.com/JPG/Shijingtu/23000/Ts/1354.jpg ## quanjingtu ?
            the720hGuide = '{}|3|2|{}|{}|{}|10|0|0|0|4|0|0|0|{}|{}|{}|{}|{}|0|{}|4.8|1|{}|{}|{}|{}| | | | | '.format(id,id,longlat[0],longlat[1],reviewnumber,reviewnumber-random.randint(100,200),random.randint(1,50),random.randint(1,10),random.randint(1,10),reviewnumber+random.randint(100,500),id,photoPath,randomTime,id)
            description = '<descripton> {} </descripton>'.format(intro)
            summary = '<summary> {} </summary>'.format(intro)
            tts = '<TTS> {} </TTS>'.format(intro)
            the720hGuide += description + summary + tts
            dict720guide.append(the720hGuide)

            # write 720/realpic/720view_search.txt:
            #name|nameEn|nameZh|nameFr|nameCN|nameEN2|nameFr2|idZh|idEn|idFr|lon|lat|x|y|lon2|lat2|x2|y2|urlSmall|urlBig|dataUrl|type|review|rank
            #崂山|laoshan|崂山|laoshan|天苑|Tianyuan|Tianyuan|170000000|0|0|120.666048|36.236447|13432483|4307950|120.658286|36.22957|13431619|4307005|https://jpartner.erlinyou.com/JPG/Shijingtu/17000/Ts/1361.jpg|https://jpartner.erlinyou.com/JPG/Shijingtu/17000_laoshan/tour.html?startscene=1|https://jpartner.erlinyou.com/JPG/Shijingtu/13432483_4307950/view_h.ddt|2|12736|4.4
            urlsmall = 'https://jpartner.erlinyou.com/JPG/Shijingtu/80000_gugong/Ts/{}.jpg'.format(id)
            urlbig = 'https://jpartner.erlinyou.com/JPG/Shijingtu/80000_gugong/tour.html?startscene={}'.format(lenoftour-1)
            urlddt = ' ' # no use
            dataUrl = 'https://jpartner.erlinyou.com/JPG/Shijingtu/80000_gugong/view_h.ddt'
            the720search = '故宫｜Forbidden City｜故宫｜Forbidden City｜{}| | |{}|0|0|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|2|{}|4.8'.format(name,id,longlat[0]-0.0001,longlat[1]-0.0001,x-20,y-20,longlat[0]+0.0001,longlat[1]+0.0001,x+20,y+20,urlsmall,urlbig,dataUrl,random.randint(500,2000))
            dict720search.append(the720search)

            #720/hModel/hModel.txt: 不需要-----?????
            #iid | adminId | type | lon | lat | x | y | scale | poiZh | poiEn | poiFr | nameZh | nameEn | nameFr | module | moduleUrl | photoUrl 
            moduleUrl = 'http://mdownload.erlinyou.com/landmark/80000/{}.ldk'.format(id)
            photoUrl = 'https://jpartner.erlinyou.com/JPG/Shijingtu/80000_gugong/T/{}.jpg'.format(id)
            the720Model = '{}|3|0|{}|{}|{}|{}|2.5|{}|0|0|{}| | |{}|{}|{}'.format(id,longlat[0],longlat[1],x,y,id,name,id,moduleUrl,photoUrl)
            dict720Model.append(the720Model)
            #1|-17000|0|120.6623827|36.2340241|13432075.00|4307617.00|2.400|6000006056|0|0|上苑仙境| | |1368|http://mdownload.erlinyou.com/landmark/-17000/1368.ldk|https://partner1.jingcailvtu.org/WEBP/Shijingtu/T/1368.jpg


#######################################
#将下载urlbegin中的全景图以及marker，保存热点数据到tour.xml文件
#######################################
def downloadPano(urlbegin,poiinfo_beginurl,saveDir,setPano,dictHotspot,dictPoiInfo,dictGuide,dict720poi,dict720guide,dict720search,dict720Model):
    if len(urlbegin)>0:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        try:
            data = s.get(urlbegin, timeout=50)
            res = data.text
        except requests.exceptions.RequestException as e:
            data = s.get(urlbegin, timeout=50)
            res =  data.text
        #res = requests.get(urlbegin)

        if data.status_code == 200:
            print(urlbegin + 'is downloading...')
            #print(res)
            result = json.loads(res)
            code = result['code']
            if code == '0' and 'data' in result.keys():
                data = result['data']
                #current pano Id
                panoId = data.get('panoId')
                northHeading = data.get('northHeading')
                curpitch = data.get('pitch')
                curname = data.get('name')
                if panoId not in setPano:
                    #if not os.path.exists(saveDir + panoId +'/'):
                    #    os.mkdir(saveDir + panoId +'/')
                    #for y in range(0,4):
                    #    for z in range(0,6*4):
                    #        urlMarker = '2_'+str(y)+'_'+str(z)+'.jpg'
                    #        urlpano = 'https://tiles-1251448083.file.myqcloud.com/'+panoId+'/cube/'+urlMarker
                    #        savePano = saveDir + panoId +'/'+ urlMarker
                    #        if not os.path.exists(savePano):
                    #            download_img(urlpano,savePano)
                    setPano.add(panoId)
                    #if not os.path.exists(saveDir + panoId +'_merge/'):
                    #    os.mkdir(saveDir + panoId +'_merge/')
                    #image_Merge_by_folder(saveDir + panoId +'/',saveDir + panoId +'_merge/')
                #marker pano Id
                print('getmarker')
                marker = data.get('marker')
                marker_rel = '<scene name="scene_{}" title="{}" onstart="" thumburl="panos/{}.tiles/thumb.jpg" lat="" lng="" heading="">'.format(panoId,curname,panoId)
                marker_rel += '<view hlookat="{}" vlookat="{}" fovtype="MFOV" fov="120" maxpiexlzoom="2.0" fovmin="70" fovmax="140" limitview="auto" />'.format(northHeading,curpitch)
                marker_rel += '<preview url="panos/{}.tiles/preview.jpg />'.format(panoId)
                marker_rel += '<image type="CUBE" multires="true" tilesize="512">'
                marker_rel += '<level tiledimagewidth="2048" tiledimageheight="2048">'
                marker_rel += '<cube url="panos/{}.tiles/s/l2/%v/l2_s_%v_%h.jpg" />'.format(panoId)
                marker_rel += '</level>'
                marker_rel += '<level tiledimagewidth="1024" tiledimageheight="1024">'
                marker_rel += '<cube url="panos/{}.tiles/s/l1/%v/l1_s_%v_%h.jpg" />'.format(panoId)
                marker_rel += '</level>'
                marker_rel += '</image>'


                markerlist = []
                for i in range(len(marker)):
                    name = marker[i].get('name')
                    heading = marker[i].get('heading')
                    pitch = marker[i].get('pitch')
                    properties = marker[i].get('properties')
                    panoId_marker = properties.get('panoId')
                    materialId = properties.get('materialId')
                    facilityId = properties.get('facilityId')
                    entityId = properties.get('entityId')
                    marker_rel += '<hotspot linkedscene="scene_{}" ath="{}" atv="{}" name="{}" onloaded="add_tooltip2(get(linkedscene),1)" />'.format(panoId_marker,heading,pitch,name)
                    urlMarker = 'https://api.show.vizen.cn/api/app/facility/marker?materialId=' + materialId + '&facilityId=' +facilityId +'&preview=0'
                    poiinfo_url = 'https://api.show.vizen.cn/api/app/entity/'+ entityId

                    if panoId_marker not in setPano:
                        downloadPano(urlMarker,poiinfo_url,saveDir,setPano,dictHotspot,dictPoiInfo,dictGuide,dict720poi,dict720guide,dict720search,dict720Model)

                marker_rel += '</scene>'
                print(marker_rel)               
                dictHotspot.append(marker_rel) 
                downloadPOIInfo(poiinfo_beginurl,saveDir,POIBeginId,dictPoiInfo,dictGuide,dict720poi,dict720guide,dict720search,dict720Model,len(dictHotspot))  
                
        else:
            print(urlbegin +' is not return!')
            
          

if __name__ == "__main__":
    IMAGE_INPUT_PATH = input("input images save forlder:")
    IMAGE_INPUT_PATH += '/'
    beginurl = 'https://api.show.vizen.cn/api/app/facility/marker?materialId=B4D46745B41D46509528234462594D25&facilityId=5aaa72ba26d67f605e9067e3&preview=0'
    poiinfo_beginurl = 'https://api.show.vizen.cn/api/app/entity/5aaa72ba26d67f605e90661f'
    #热点关系,tour.xml
    setFind = set()
    dictHotspot = []
    #生成故宫的poi，guide，720等数据
    dictPoiInfo = []
    dictGuide  = []
    dict720poi = []
    dict720guide  = []
    dict720search =  []
    dict720Model = []
    #抓取数据
    downloadPano(beginurl,poiinfo_beginurl,IMAGE_INPUT_PATH,setFind,dictHotspot,dictPoiInfo,dictGuide,dict720poi,dict720guide,dict720search,dict720Model)

    #存储热点关系
    with open(IMAGE_INPUT_PATH +'hotspot.txt',"w") as f:
        f.write(str(dictHotspot))

    ##############poi & guide ##########
    folder = IMAGE_INPUT_PATH + 'poi-guide/'
    if not os.path.exists(folder):
        os.mkdir(folder)
    #poi
    poi_folder = folder+'poi/'
    if not os.path.exists(poi_folder):
        os.mkdir(poi_folder)
    with open(poi_folder +'poi.txt',"w") as f:
        f.write(str(dictPoiInfo))
    #guide
    guideinfo_folder = folder+'guideinfo/'
    if not os.path.exists(guideinfo_folder):
        os.mkdir(guideinfo_folder)
    with open(guideinfo_folder +'guide.txt',"w") as f:
        f.write(str(dictGuide))
    #############720########
    folder = IMAGE_INPUT_PATH + '720/'
    if not os.path.exists(folder):
        os.mkdir(folder)
    #hpoi
    hpoi_folder = folder+'hpoi/'
    if not os.path.exists(hpoi_folder):
        os.mkdir(hpoi_folder)
    with open(hpoi_folder +'hpoi.txt',"w") as f:
        f.write(str(dict720poi))
    #hguide
    hguide_folder = folder+'hguide/'
    if not os.path.exists(hguide_folder):
        os.mkdir(hguide_folder)
    with open(hguide_folder +'hguide.txt',"w") as f:
        f.write(str(dict720guide))
    #hsearch
    hsearch_folder = folder+'realpic/'
    if not os.path.exists(hsearch_folder):
        os.mkdir(hsearch_folder)
    with open(hsearch_folder +'720view_search.txt',"w") as f:
        f.write(str(dict720search))
    #hmodel
    hModel_folder = folder+'hModel/'
    if not os.path.exists(hModel_folder):
        os.mkdir(hModel_folder)
    with open(hModel_folder +'hModel.txt',"w") as f:
        f.write(str(dict720Model))
    print('结束！')
