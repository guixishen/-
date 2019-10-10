#  -*-coding:utf8 -*-
import requests
from bs4 import BeautifulSoup
from urllib import request
from http import cookiejar
import math
import pandas
import time
from tqdm import tqdm

#爬取中华灯谜库谜题

URL = ''

# 声明一个CookieJar对象实例来保存cookie
cookie = cookiejar.CookieJar()
# 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
handler = request.HTTPCookieProcessor(cookie)
# 通过CookieHandler创建opener
opener = request.build_opener(handler)
# 此处的open方法打开网页
response = opener.open(URL)
# 获取cookie信息
for item in cookie:
    name = item.name
    value = item.value

Cookie = name + '=' + value

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Host':'www.zhgc.com',
    'Cookie':Cookie,
    'Upgrade-Insecure-Requests':'1'
}

dmlist = []

res = requests.post(URL,headers=headers)
res.encoding = 'gb18030'
soup = BeautifulSoup(res.text.replace('&nbsp;',''),'lxml')
soup = soup.select('font')[2].text
cnt = ''.join(soup)
cnt = int(cnt.split('共')[1].split('条')[0])
PageCnt = math.ceil(cnt/50) #向上取整得出总页数
# print(PageCnt)

def getDm(data):
    res = requests.post(URL,headers=headers,data=data)
    res.encoding = 'gb18030'
    soup = BeautifulSoup(res.text.replace('&nbsp;',''),'lxml')
    dm = soup.select('#AutoNumber1 tr')
    for d in dm[1:len(dm)]:
         d = d.text.split('\n')[1:8]
         dmlist.append(d)
    return dmlist

for i in tqdm(range(PageCnt,0,-1)):
    data = {
        'pxfs': '2',
        'jls': '50',
        'jumpPage': str(i)
    }
    getDm(data)
    time.sleep(1)

df = pandas.DataFrame(dmlist)
df.columns = ['谜面','谜目/谜格','谜底','作者','备注','发表时间','来源说明']
df.to_excel('谜题.xlsx',index=False)
print('下载已完成！')
