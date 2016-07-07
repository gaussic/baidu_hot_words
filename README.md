## 百度的新闻热搜词抓取

原网址为：[http://news.baidu.com/n?cmd=1&class=reci](http://news.baidu.com/n?cmd=1&class=reci)

具体抓取详情见：[Gaussic博客](http://my.oschina.net/gaussik/blog/707998)


### 接口与参数

接口的 base_url 为 'http://news.baidu.com/n?m=rddata&v=hot_word',

带两个参数

- type：0(全部)、2(国内)、1(国际)、5(社会)、14(军事)、6(财经)、10(汽车)、8(科技)、4(娱乐)、3(体育)
- date：格式为 20160703、20160704、20160705，以此类推

### 使用 requests 抓取关键词数据:

```
import requests
from bs4 import BeautifulSoup
import urllib

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
```

输出结果：

```
http://news.baidu.com/n?m=rddata&v=hot_word&type=0
习近平会见联合国秘书长
习近平会见巴布亚新几内亚总理
东南沿海将迎暴雨
南京南动车所塌方
湖南暴雨过后各地频频捡到大鱼
6.6亿造诺亚方舟
带4000元钱穷游中国
好声音更名
葡萄牙2-0威尔士进决赛
霍建华林心如婚礼没请胡歌
中国正式加入国际移民组织
房地产税法最快2017年通过
43人中国旅行团护照在瑞典被抢
长江中下游水位全线超警
上海垃圾偷倒太湖
里约奥运计划发900万避孕套
孕妇被赶下车产子剧情反转
开车吃棒冰被罚
胡歌祝福霍建华林心如结婚
万科A跌停
陈晓陈妍希领证
林心如霍建华宣布婚期
交通违规优惠券
朱诺进入木星轨道
4000吨垃圾偷运太湖
合建马六甲港口
61岁高龄产妇产子
男子4年写150万字日记给亡妻
江苏等6省区将有大暴雨
湖北多地降雨量百年一遇
```

### 添加日期参数

日期格式为 YYYYMMDD，如 20160703

```
hot_type = '2'
hot_date = '20160705'

parameters = {'type': hot_type, 'date': hot_date}

# 获取 JSON 数据
r = requests.get(base_url, params=parameters)
print(r.url)

hot_words_dict = r.json()

# 输出热搜关键词
for hot_word in hot_words_dict.get('data'):
    print(hot_word.get('query_word'))
```

输出结果：

```
http://news.baidu.com/n?m=rddata&v=hot_word&type=2&date=20160705
金价5连涨创新高
结婚没嫁妆遭轮奸
乡村小学减员潮
最帅交警一夜成网红
宜家回应商场裸照门
男子拿驾照喜极而泣
陈冠希晒近照苍老
身份证异地办理
10岁男童重192公斤
女特工过110岁生日
10省区市大暴雨
一批新规明日起实施
防二手烟神器
扶贫大会上演全武行
医院雇人骗医保
胚胎沉睡18年被唤醒
京城商圈大尺度雕塑
少年开发机器人律师
香港迪士尼每况愈下
北影毕业照美女如云
球场上钓鱼打枪
少女被关铁笼成性奴
单身汪娶手机当老婆
孙俪12岁起恨透父亲
学生当街看色情片
杰克逊家中物品曝光
贵州特大暴雨
太阳的后裔拍中国版
国足复制冰岛奇迹
周杰伦胖13公斤
```

### 按关键词抓取新闻

基本url为 http://news.baidu.com/ns?tn=news ,接参数word为 JSON 数据的 query_word 字段。

```
query_word = '43人中国旅行团护照在瑞典被抢'    
news_base_url = 'http://news.baidu.com/ns?tn=news'

news_url = news_base_url + query_word
parameters = {'word': query_word}

# 获取 JSON 数据
r = requests.get(news_base_url, params=parameters)
print(r.url)

soup = BeautifulSoup(r.text, 'lxml')
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

for news in news_list:
    print(news)
```

输出结果：

```
http://news.baidu.com/ns?tn=news&word=43%E4%BA%BA%E4%B8%AD%E5%9B%BD%E6%97%85%E8%A1%8C%E5%9B%A2%E6%8A%A4%E7%85%A7%E5%9C%A8%E7%91%9E%E5%85%B8%E8%A2%AB%E6%8A%A2
{'链接': 'http://news.ifeng.com/a/20160706/49300638_0.shtml', '来源': '凤凰网', '发布日期': '2016年07月06日', '标题': '43人中国旅行团护照在瑞典被抢'}
{'链接': 'http://bj.people.com.cn/n2/2016/0706/c233086-28617563.html', '来源': '人民网', '发布日期': '2016年07月06日', '标题': '43人中国旅行团护照瑞典被抢 旅行社将负责赔偿'}
{'链接': 'http://www.dzwww.com/xinwen/shehuixinwen/201607/t20160706_14581063.htm', '来源': '大众网', '发布日期': '2016年07月06日', '标题': '在瑞典吃饭时突然护照被抢 43名中国游客无奈回国'}
{'链接': 'http://news.shm.com.cn/2016-07/06/content_4497629.htm', '来源': '水母网', '发布日期': '2016年07月06日', '标题': '43人中国旅行团护照在瑞典被抢 游客正分批回国'}
{'链接': 'http://new.qi-che.com/shehuiredia/xinwen-20160706270778.html', '来源': '汽车中国', '发布日期': '2016年07月06日', '标题': '今日头条新闻43人中国旅行团护照在瑞典被抢劫丢失 正分批回国最'}
{'链接': 'http://news.k618.cn/society/rd/201607/t20160706_7981118.html', '来源': '未来网', '发布日期': '2016年07月06日', '标题': '43人中国旅行团护照瑞典被抢 旅行社将负责赔偿'}
{'链接': 'http://www.rmzxb.com.cn/c/2016-07-06/903304.shtml?n2m=1', '来源': '人民政协网', '发布日期': '2016年07月06日', '标题': '中国43人旅行团在瑞典被抢 所有人护照丢失 (1)'}
{'链接': 'http://news.jschina.com.cn/system/2016/07/06/029103019.shtml', '来源': '中国江苏网', '发布日期': '2016年07月06日', '标题': '43人中国旅行团护照瑞典被抢 旅行社将负责赔偿'}
```