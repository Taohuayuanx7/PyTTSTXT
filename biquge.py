import time
import random
import sys
import urllib
import requests
import os
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666 Edg/108.0.0.0'}
           
# 搜索小说
def search_book(search_book_name):
    
    try:
        if search_book_name:

            new_search_book_name = urllib.parse.quote(search_book_name)

            search_url = 'http://www.b520.cc/modules/article/search.php?searchkey=' + new_search_book_name
           
            novel_source = requests.get(search_url,headers=headers).text
            res=requests.get(search_url,headers=headers)
            print(res.status_code)
            search_soup = BeautifulSoup(novel_source, "lxml")

            search_book_url = search_soup.find("div", id="hotcontent").find_all("td", class_="odd")

            if len(search_book_url) > 0:
                for item in search_book_url:
                    if item.text == search_book_name:
                        book_url = item.find("a").get('href')
                        return book_url

            else:
                print("未找到您要搜索的小说!")

        else:
            print("请输入小说名称")
    except Exception as e:
        print(e)
    

# 获取小说名称和下面各个章节的url地址
def get_all_chapter_href(search_url):
        
    try:
        if search_url:

            new_search_url = requests.get(search_url,headers=headers)

            # 通过F12查看笔趣阁小说页面html结构发现meta标签上gbk格式解析的，所以在这里转一下
            new_search_url.encoding = "gbk"

            chapter_soup = BeautifulSoup(new_search_url.text, "lxml")

            chapter_list = chapter_soup.find("div", id="list").find_all("a")
            #print(chapter_list)
            booktitle = chapter_soup.find("div", id="maininfo").find("div", id="info").find("h1")
            print("正在下载的小说名称是: " + booktitle.text)            

            href_list = []

            for a in chapter_list:

                href_list.append(a.get('href'))
            
            return href_list, booktitle
        else:
            return None, None

    except Exception as e:
        print(e)
#注意这里 开始章节


# 获取每个章节下的内容并下载到txt
def get_chapter_content(href_list,booktitle):
    if not os.path.exists("E:/" + booktitle.text):
        os.makedirs("E:/" + booktitle.text)
    try:
        if href_list != None and booktitle != None:
            for i in range(start ,len(href_list)):
                url=href_list[i]

                # 如果连接太过频繁会报错,所以这里用sleep休眠方式
                
                time.sleep(1 + random.random())
                chapter_url = requests.get(url,headers=headers)

                chapter_url.encoding = "gbk"

                text = chapter_url.text

                content_soup = BeautifulSoup(text, "lxml")

                bookname = content_soup.find("div", class_="bookname").find("h1")

                content = content_soup.find_all("div", id="content")[0].find_all("p")
                newbookname=bookname.text.replace('?','')
                if not os.path.exists("E:/" + booktitle.text + "/" + newbookname +  ".txt"):
                   
                    with open("E:/" + booktitle.text + "/" +str(i)+" "+ newbookname +  ".txt",'a', encoding='utf-8') as f:

                        f.write(bookname.text + "\n\r\r")
                        print("正在下载的章节名称是: " + bookname.text +" "+ str(i))

                        for book in content:

                            f.write(book.text + "\n\r")
                else:
                    print("正在跳过的章节名称是: " + bookname.text +" "+ str(i))
        
        else:
            return 

    except Exception as e:
        print(e)

if __name__ == "__main__":

    #search_book_name = input("请输入想要下载的小说名称: ")

    #search_url = search_book(search_book_name)
    search_url=input("请输入下载的地址:")
    start=int(input("请输入开始下载章节:"))
    if start==None:
        start=1
    #print(search_url)
    
    
    href, booktitle = get_all_chapter_href(search_url)

    get_chapter_content(href,booktitle)