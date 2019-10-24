

import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os
import img2pdf
import click
import requests
from urllib.parse import quote



def get_soup(url):  

    try:
        response = urllib.request.urlopen(url,timeout=10)  # 请求网页，返回句柄
        page = response.read()  # 读取并返回网页内容
        # print(page)
        soup = BeautifulSoup(page,"lxml")
        return soup

    except Exception as e:
        print(e) 
        print(url) 



def find_image_url_and_name(soup):

    div = soup.find("div",{"class":"imgtab maintabview"})
    pics = div.find_all("img")

    images_list = []
    for pic in pics:
        images ={}
        image_url = pic["src"][:-10]
       
        image_name = pic["alt"]
        images["name"] = image_name
        images["url"] = image_url
        images_list.append(images)
    return images_list

def save_images(images_list,tab_id):

    dirname = tab_id
    os.mkdir(dirname)

    file_path_name_list = []
    for i,images in enumerate(images_list):

        print(i,images["name"])
        image_format = images["url"].split(".")[-1]
        file_name = str(i)
        file_path_name = dirname + "/" + file_name +"." + image_format
        print(file_path_name)
        file_path_name_list.append(file_path_name)
        urlretrieve(images["url"], file_path_name)

    return file_path_name_list

@click.group()
def guitar_dl():
    pass

@click.command()
@click.option('--url', help='the url of one guitar tab')
def download(url):

    """A tools for download tabs from jitashe.org """

    # url = "https://www.jitashe.org/tab/9895/"
    tab_id =  url.split("/")[-2]

    soup = get_soup(url)
    images_list = find_image_url_and_name(soup)
    tab_name = images_list[0]["name"].replace(":","_")[:-6]


    print("Downloading %s "%tab_name)
    print("*"*60)
    file_path_name_list = save_images(images_list,tab_id)

    print("*"*60)
    print("Converting to pdf...")
    print(file_path_name_list)
    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt)
    print(tab_name)
    with open(tab_name + ".pdf", "wb") as f:
        f.write(img2pdf.convert(file_path_name_list, layout_fun=layout_fun))
    print("Done!")



def parse_tab(tab_div):

    result = {}
    title = tab_div.find("a",{"class":"title"})
    url = title["href"]
    text = title.text

    tag_list = tab_div.find("div",{"class":"taglist"})
    tags = tag_list.text

    result["title"] = text
    result["url"] = "https://www.jitashe.org" + url
    result["tags"] = tags

    return result

def find_search_result(soup):
    
    div = soup.find("div",{"class":"tab-list"})
    # print(div)
    tab_divs = div.find_all("div",{"class":"tab-item"})

    result_list = []
    for tab_div in tab_divs:
        result = parse_tab(tab_div)
        result_list.append(result)

    return result_list

@click.command()
@click.option('--keywords', help='the keywords you want to search')
def search(keywords):
    ''' search tabs from jitashe.org'''
    url_base = "https://www.jitashe.org/search/tab/%s/"

    # param = {"wd": "莫烦Python"}  # 搜索的信息
    # r = requests.get('http://www.baidu.com/s', params=param)
    # print(r.url)
    url = url_base%quote(keywords)
    soup = get_soup(url)
    # print(soup)

    result_list = find_search_result(soup)
    result_list = [item for item in result_list if "图片谱" in item["tags"]]
    for i,item in enumerate(result_list):
        print("-"*60)
       
        print(i,item["url"],item["title"],item["tags"].replace("\n"," "))

    # print(result_list)


guitar_dl.add_command(download)
guitar_dl.add_command(search)


if __name__ == '__main__':
    guitar_dl()
    # cli()


    # urls = [
    # # "https://www.jitashe.org/tab/14626/",
    # # "https://www.jitashe.org/tab/1299551/",
    # "https://www.jitashe.org/tab/14435/",
    # # "https://www.jitashe.org/tab/1340565/",
    # # "https://www.jitashe.org/tab/1307674/",
    # # "https://www.jitashe.org/tab/9933/",
    # # "https://www.jitashe.org/tab/9132/",
    # # "https://www.jitashe.org/tab/67507/",
    # # "https://www.jitashe.org/tab/1335746/",
    # # "https://www.jitashe.org/tab/9851/",
    # # "https://www.jitashe.org/tab/93549/"
    # ]

    # # for url in urls:
    # #     print(url)
    # #     guitar_dl(url)
    # search_tabs("女儿情")
# ------------------------------

# download 有谱么




