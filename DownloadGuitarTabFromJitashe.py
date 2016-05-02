
# coding: utf-8

import urllib.request
import datetime
from bs4 import BeautifulSoup
import re
from os import mkdir
import chardet
BASE_URL = 'http://www.jitashe.net'


def get_soup(url):  

    try:
        response = urllib.request.urlopen(url,timeout=10)  # 请求网页，返回句柄
        page = response.read()  # 读取并返回网页内容
        # print(page)
        soup = BeautifulSoup(page)
        return soup

    except Exception as e:
        print(e) 
        print(url) 

def find_all_alblum_name(soup):

    album_list=[]
    albumlist = soup.findAll('a',{'class':'CDcover100'})
    for album_li in albumlist:
        album={}
        album['url']= BASE_URL + album_li['href']
        album['name'] = album_li['title']
        album_list += [album]   
        
    return album_list


def find_song_url(url):
    
    song_list = []
    response = urllib.request.urlopen(url,timeout=10)  # 请求网页，返回句柄
    page = response.read()  # 读取并返回网页内容
    
    regular = b'''<div class='song_info'>[\s\S]{10,300}</div>'''
    pattern = re.compile(regular)
    song_div_list = pattern.findall(page)
    for song in song_div_list:   
        asong={}
        soup = BeautifulSoup(song)
        song = soup.find('a')
        asong['url']=BASE_URL + song['href']
        asong['name']=song.text
        song_list +=[asong]
    return song_list

def find_all_alblum_list(artist_code):
    baseUrl = 'http://www.jitashe.net/album/list/' + artist_code
    soup= get_soup(baseUrl)
    album_name_list =  find_all_alblum_name(soup)
    album_list=[]
    for item  in album_name_list:
        url = item['url']
        temp={}
        song_list = find_song_url(url)
        temp['album']= item['name']
        temp['datial']=song_list
        album_list+=[temp]
    return album_list

def get_tab_url(url):
    tab_list = []
    
    response = urllib.request.urlopen(url,timeout=10)  # 请求网页，返回句柄
    page = response.read()  # 读取并返回网页内容

    # file_hander = open('page.html','w')
    # file_hander.write(page.decode('utf-8'))
    # file_hander.close()

    # print(len(page))
    regular = b'''<div class="bm_c tablist">[\s\S]*<div class="bm" id="album_summary">'''

    pattern = re.compile(regular)
    # print(len(pattern.findall(page)))
    tab_div = pattern.findall(page)[0].strip(b'''div class="bm" id="album_summary">''')
    tab_div = BeautifulSoup(tab_div) 
    tablist = tab_div.findAll('a',{'class':'xst'})

    icn = tab_div.findAll('td',{'class':'icn'})
    tab_type = [item.find('img') for item in icn]
    # tab_type = tab_div.findAll('img')
#     print(tab_type) 
    for item,type_ in zip(tablist,tab_type):
        tab={}
        tab['url'] = BASE_URL+item['href']
        tab['type'] = type_['title']
        tab_list += [tab]        
    return tab_list

def get_img_url(url):
    img_list = []
    
    response = urllib.request.urlopen(url,timeout=10)  # 请求网页，返回句柄
    page = response.read()  # 读取并返回网页内容

    # file_hander = open('page.html','w',encoding='UTF-8',)
    # # print(chardet.detect(page)) 
    # file_hander.write(page.decode('utf-8'))
    # file_hander.close()

    regular = b'''<div class="imgtab">[\s\S]*<a name="forDownload" id="forDownload"></a>'''
    pattern = re.compile(regular)
    img_div = pattern.findall(page)[0].strip(b'''<a name="forDownload" id="forDownload"></a>''')
    img_div = BeautifulSoup(img_div) 
    imglist = img_div.findAll('img')
    for item in imglist:
#         print(item) 
        img={}
        img['url'] = BASE_URL+'/'+item['file']
        img_list += [img]
        
    return img_list

'''
抓取网页文件内容，保存到内存
'''
def get_file(url):
    try:
        response = urllib.request.urlopen(url,timeout=10)  # 请求网页，返回句柄
        data=response.read()
        return data
    except BaseException as e:
        print(e) 
        return None
    
'''
保存文件到本地
@path  本地路径
@file_name 文件名
@data 文件内容
'''
def save_file(path, file_name, data):
    if data == None:
        return
    
    if(not path.endswith("/")):
        path=path+"/"
    file=open(path+file_name, "wb")
    file.write(data)
    file.flush()
    file.close()
    

def download_asong_tab(song_album,song_name,song_url):
    tab_url = get_tab_url(song_url)
    for j,item in enumerate(tab_url):
        # print('getting tab .............'+str(j))
        if item['type'] !='图片谱':
            print('GTP tab be passed........'+str(j))
            continue

        print('getting tab .............'+str(j))


        imgurl = item['url']
        img = get_img_url(imgurl)
        for i,jpg_url in enumerate(img):
            file_data = get_file(jpg_url['url'][:-10]) 
            file_name=song_name+'版本'+str(j+1)+'_'+str(i+1)+'.jpg'
            save_file(song_album, file_name, file_data)



def download_all_album(all_alblum):
    for album in all_alblum:

        print('downloading album ',album['album']) 
        print('*'*50) 
        album_name=album['album']
        for song in album['datial']:
            song_name=song['name']
            song_url=song['url']
            print('downloading song ',song_name)
            try:
                download_asong_tab(album_name,song_name,song_url)
                # print('downloading song ',song_name,'sucessed!!') 
            except Exception as e:
                print('downloading song ',song_name,'error!',e) 
     

#######################################################################################


## 获取专辑列表

artist_code = '4447'

print('preparing...') 
all_alblum = find_all_alblum_list(artist_code)
# for item in album_list:
#     mkdir(item['album'])

download_all_album(all_alblum)







