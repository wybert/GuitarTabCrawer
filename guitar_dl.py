

import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os
import img2pdf
import click


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



@click.command()
@click.option('--url', help='the url of one guitar tab')
def guitar_dl(url):

    """A tools for download tabs from jitashe.org """

    # url = "https://www.jitashe.org/tab/9895/"
    tab_id =  url.split("/")[-2]

    soup = get_soup(url)
    images_list = find_image_url_and_name(soup)
    tab_name = images_list[0]["name"][:-6]


    print("Downloading %s "%tab_name)
    print("*"*60)
    file_path_name_list = save_images(images_list,tab_id)

    print("*"*60)
    print("Converting to pdf...")
    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt)
    with open(tab_name + ".pdf", "wb") as f:
        f.write(img2pdf.convert(file_path_name_list, layout_fun=layout_fun))
    print("Done!")

if __name__ == '__main__':
    guitar_dl()