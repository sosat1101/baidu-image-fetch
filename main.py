# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 12:40:24 2017

@author: guomei007
"""

import json
import itertools
import urllib
import requests
import os
import re
import sys

str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
char_table = {ord(key): ord(value) for key, value in char_table.items()}


# 解码图片URL
def decode(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)


# 生成网址列表
def buildUrls(word):
    word = urllib.parse.quote(word)  # 例如：将“汽车”转换成“%E6%B1%BD%E8%BD%A6”
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={" \
          r"word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60 "
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls


# 解析JSON获取图片URL
re_url = re.compile(r'"objURL":"(.*?)"')


def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls


def downImg(imgUrl, dirpath, imgName):
    filename = os.path.join(dirpath, imgName)
    try:
        res = requests.get(imgUrl, timeout=15)
        if str(res.status_code)[0] == "4":
            print(str(res.status_code), ":", imgUrl)
            return False
    except Exception as e:
        print(" This is Exception：", imgUrl)
        print(e)
        return False
    with open(filename, "wb") as f:
        f.write(res.content)
    return True


def mkDir(dirName):
    dirpath = os.path.join(sys.path[0], dirName)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath


if __name__ == '__main__':
    print("Welcome !!! \n Now, it only one word")
    print("Download in results")
    print("=" * 50)
    word = input("Please input your word:")
    count = int(input("请输入图片数量:"))
    dirpath = mkDir("百度图片下载")

    urls = buildUrls(word)

    index = 0
    flag = True
    for url in urls:
        print("requesting：", url)
        html = requests.get(url, timeout=10).content.decode('utf-8')
        imgUrls = resolveImgUrl(html)
        if len(imgUrls) == 0:  # 没有图片则结束
            break
        for url in imgUrls:
            if downImg(url, dirpath, str(index) + ".jpg"):
                index += 1
                print("Downloaded %s picture" % index)
            if index >= count:
                flag = False
                break
        if flag == False:
            break

'''
url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%B5%B7%E8%B4%BC%E7%8E%8B&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word=%E6%B5%B7%E8%B4%BC%E7%8E%8B&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&pn=30&rn=30&gsm=1e&1502108303234='
res = requests.get(url)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')
jd = json.loads(soup.text)#将文本转换成字典对象
data = jd['data']
print(data[1]['replaceUrl'])

for i in range(0, len(data)-1):
    print(data[i])#[1]['ObjURL']
'''
