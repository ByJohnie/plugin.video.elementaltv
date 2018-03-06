# -*- coding: utf-8 -*-
#Библиотеки, които използват python и Kodi в тази приставка
import re
import sys
import os
import urllib
import urllib2
import xbmc, xbmcplugin,xbmcgui,xbmcaddon
import base64
import cookielib
import json
import datetime

#Място за дефиниране на константи, които ще се използват няколкократно из отделните модули
__addon_id__= 'plugin.video.elementaltv'
__Addon = xbmcaddon.Addon(__addon_id__)
__settings__ = xbmcaddon.Addon(id=__addon_id__)
__icon__ =  xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/icon.png")
logos = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/logos/")
username = xbmcaddon.Addon().getSetting('settings_username')
password = xbmcaddon.Addon().getSetting('settings_password')
MUA = 'Mozilla/5.0 (Linux; Android 5.0.2; bg-bg; SAMSUNG GT-I9195 Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19' #За симулиране на заявка от мобилно устройство
UA = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0' #За симулиране на заявка от  компютърен браузър
login = base64.b64decode("aHR0cHM6Ly9wbGF5LmVsZW1lbnRhbC50di92MS91c2Vycy9sb2dpbg==")
kanal = base64.b64decode("aHR0cHM6Ly9wbGF5LmVsZW1lbnRhbC50di92MS9jaGFubmVscw==")
play = base64.b64decode("aHR0cHM6Ly9wbGF5LmVsZW1lbnRhbC50di92MS9wbGF5bGlzdHMv")
secondplay = base64.b64decode("L3BsYXlsaXN0Lm0zdTg/YmVnaW49")
secondstop = base64.b64decode("JmVuZD0=")
thirdplay = base64.b64decode("JmFjY2Vzc190b2tlbj0=")
baseurl = base64.b64decode("aHR0cHM6Ly9wbGF5LmVsZW1lbnRhbC50dg==")
#инициализация
if not username or not password or not __settings__:
        xbmcaddon.Addon().openSettings()


params = {"email":username,"password":password,"grant_type":"client_credentials"}
try:
 req = urllib2.Request(login, json.dumps(params))
 req.add_header('User-Agent', UA)
 cj = cookielib.CookieJar()
 opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
 f = opener.open(req)
 jsonrsp = json.loads(f.read())
 status = jsonrsp['status']
 token =  jsonrsp['data']['access_token']
 bearer = jsonrsp['data']['token_type']
 dataA = bearer + " " + token
 #if status == 200:
 # xbmc.executebuiltin(('Notification(%s,%s,%s,%s)' % (status, 'Успешен Вход в системата', '1000', __icon__)))
except urllib2.URLError, e:
 xbmc.executebuiltin(('Notification(%s,%s,%s,%s)' % (e, 'Най-вероятно грешни данни', '2000', __icon__)))



#Меню с директории в приставката
def CATEGORIES():
        addDir('Телевизия',kanal,1,'DefaultFolder.png')
        addDir('Записи',kanal,2,'DefaultFolder.png')

#Разлистване видеата на първата подадена страница
def INDEXPAGES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        req.add_header("Authorization", dataA)
        req.add_header('Referer', login)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        f = opener.open(req)
        data = f.read()
        #f.close()
        match = re.compile('access":1,"id":"(.+?)","resolution":"(.+?)x(.+?)","currentepg":.+?start":(\d+).+?title":"(.+?)".+?"chanName":"(.+?)"').findall(data)
        for chid,width,height,starttimer,epgtitle,chname in match:
         thumbnail = logos + chname.replace(' ','-').replace('Канал-3','Kanal-3').replace('ТВ-Европа','TV-Europe')+'.png'
         link = play + chid + secondplay + starttimer + thirdplay + token
         if height == '720':
          addLink(chname,link,4,epgtitle,thumbnail)
         if height == '576':
          addLink2(chname,link,4,epgtitle,thumbnail)

def ZAPISI(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        req.add_header("Authorization", dataA)
        req.add_header('Referer', login)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        f = opener.open(req)
        data = f.read()
        f.close()
        addDir('Филми и Сериали', baseurl + '/v1/epgs/categories/100',3,'DefaultFolder.png')
        addDir('Новини', baseurl + '/v1/epgs/categories/110',3,'DefaultFolder.png')
        addDir('Шоу', baseurl + '/v1/epgs/categories/120',3,'DefaultFolder.png')
        addDir('Спорт', baseurl + '/v1/epgs/categories/130',3,'DefaultFolder.png')
        addDir('Детски', baseurl + '/v1/epgs/categories/140',3,'DefaultFolder.png')
        addDir('Музикални', baseurl + '/v1/epgs/categories/150',3,'DefaultFolder.png')
        addDir('Културни', baseurl + '/v1/epgs/categories/160',3,'DefaultFolder.png')
        addDir('Публицистика', baseurl + '/v1/epgs/categories/170',3,'DefaultFolder.png')
        addDir('Образование и наука', baseurl + '/v1/epgs/categories/180',3,'DefaultFolder.png')
        addDir('Хоби и туризъм', baseurl + '/v1/epgs/categories/190',3,'DefaultFolder.png')
        addDir('Други', baseurl + '/v1/epgs/categories/210',3,'DefaultFolder.png')


def INDEXZAPISI(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        req.add_header("Authorization", dataA)
        req.add_header('Referer', url)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        f = opener.open(req)
        data = f.read()
        f.close()
        match = re.compile('start":(.+?),"stop":(.+?),"title":"(.+?)","subtitle":"(.+?)".+?chan_id":"(.+?)","chan_name":"(.+?)"').findall(data)
        for start,stop,title,subtitle,chid,chname in match:
         thumbnail = logos + chname.replace(' ','-').replace('Канал-3','Kanal-3').replace('ТВ-Европа','TV-Europe')+'.png'
         link = play + chid + secondplay + start + secondplay + stop + thirdplay + token
         vremeto = datetime.datetime.fromtimestamp(int(start)).strftime('%d.%m.%Y %H:%M')
         name = chname + ' ' + title + ' ' + vremeto
         addLink(name,link,4,subtitle,thumbnail)




#Зареждане на видео
def PLAY(url):
        li = xbmcgui.ListItem(iconImage=iconimage, thumbnailImage=iconimage, path=url+'|User-Agent='+urllib.quote_plus(UA))
        li.setInfo('video', { 'title': name })
        try:
         xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
        except:
         xbmc.executebuiltin("Notification('Грешка','Видеото липсва на сървъра!')")




#Модул за добавяне на отделно заглавие и неговите атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addLink(name,url,mode,plot,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": plot } )
        liz.addStreamInfo('video', { 'width': 1280, 'height': 720 })
        liz.addStreamInfo('video', { 'aspect': 1.78, 'codec': 'h264' })
        liz.addStreamInfo('audio', { 'codec': 'aac', 'channels': 2 })
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addLink2(name,url,mode,plot,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": plot } )
        liz.addStreamInfo('video', { 'width': 1024, 'height': 576 })
        liz.addStreamInfo('video', { 'aspect': 1.78, 'codec': 'h264' })
        liz.addStreamInfo('audio', { 'codec': 'aac', 'channels': 2 })
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

#Модул за добавяне на отделна директория и нейните атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


#НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param







params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        name=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass


#Списък на отделните подпрограми/модули в тази приставка - трябва напълно да отговаря на кода отгоре
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
    
elif mode==1:
        print ""+url
        INDEXPAGES(url)

elif mode==2:
        print ""+url
        ZAPISI(url)

elif mode==3:
        print ""+url
        INDEXZAPISI(url)

elif mode==4:
        print ""+url
        PLAY(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
