
# coding: utf-8

# ## 百度新闻热搜词抓取
# 
# 原抓取网址为：[http://news.baidu.com/n?cmd=1&class=reci](http://news.baidu.com/n?cmd=1&class=reci)
# 
# Github代码：[点击访问](https://github.com/gaussic/baidu_hot_words)
# 
# #### 接口与参数
# 
# 接口的 `base_url` 为 [http://news.baidu.com/n?m=rddata&v=hot_word](http://news.baidu.com/n?m=rddata&v=hot_word)
# 
# 带两个参数
# 
# - type：0(全部)、2(国内)、1(国际)、5(社会)、14(军事)、6(财经)、10(汽车)、8(科技)、4(娱乐)、3(体育)
# - date：格式为 20160703、20160704、20160705，以此类推
# 
# #### 使用 requests 抓取关键词数据:

# In[1]:

import requests  
from bs4 import BeautifulSoup


# In[2]:

# 基本Url
base_url = 'http://news.baidu.com/n?m=rddata&v=hot_word'  
hot_type = '0'

parameters = {'type': hot_type}

# 获取 JSON 数据
r = requests.get(base_url, params=parameters)  
print(r.url)

hot_words_dict = r.json()

# 输出热搜关键词
for hot_word in hot_words_dict.get('data'):  
    print(hot_word.get('query_word'))


# ### 添加日期参数
# 
# 日期格式为 YYYYMMDD，如 20171122

# In[3]:

hot_type = '2'   # 国内
hot_date = '20171122'

parameters = {'type': hot_type, 'date': hot_date}

# 获取 JSON 数据
r = requests.get(base_url, params=parameters)  
print(r.url)

hot_words_dict = r.json()

# 输出热搜关键词
for hot_word in hot_words_dict.get('data'):  
    print(hot_word.get('query_word'))


# ### 按关键词抓取新闻
# 
# 基本url为 [http://news.baidu.com/ns?tn=news](http://news.baidu.com/ns?tn=news)， 接参数 word 字段。

# In[4]:

query_word = '香港将迎首位女特首'  
news_base_url = 'http://news.baidu.com/ns?tn=news'

parameters = {'word': query_word}

# 获取 JSON 数据
r = requests.get(news_base_url, params=parameters)  
print(r.url)

soup = BeautifulSoup(r.text, 'lxml')   # lxml可以换成其他解析库
news_html_list = soup.select('div.result')  
news_list = []  
for news_html in news_html_list:  
    news = {}
    news['标题'] = news_html.a.get_text().strip()
    news['链接'] = news_html.a['href']
    source = news_html.find('p', 'c-author').get_text().strip().replace('\xa0\xa0', ' ').split(' ')
    news['来源'] = source[0]
    news['发布日期'] = source[1]

    news_list.append(news)

import json
for news in news_list:
    print(json.dumps(news, ensure_ascii=False))

