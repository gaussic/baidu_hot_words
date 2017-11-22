## 百度新闻热搜词抓取

原抓取网址为：[http://news.baidu.com/n?cmd=1&class=reci](http://news.baidu.com/n?cmd=1&class=reci)

Github代码：[点击访问](https://github.com/gaussic/baidu_hot_words)

#### 接口与参数

接口的 `base_url` 为 [http://news.baidu.com/n?m=rddata&v=hot_word](http://news.baidu.com/n?m=rddata&v=hot_word)

带两个参数

- type：0(全部)、2(国内)、1(国际)、5(社会)、14(军事)、6(财经)、10(汽车)、8(科技)、4(娱乐)、3(体育)
- date：格式为 20160703、20160704、20160705，以此类推

<!-- more -->

#### 使用 requests 抓取关键词数据:

```python
import requests  
from bs4 import BeautifulSoup

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
习近平回信勉励[br]乌兰牧骑队员
习近平致丝路沿线民间合作网络论坛贺信
头颅[br]移植手术成功
济州岛[br]迎中旅游团
2018[br]全球强震或增
趴折叠床[br]辅导学生
国产直升机试飞成功
中国在太平洋岛国投资基建
无人售货纸箱亮相西南大学
惠普CEO惠特曼将于明年初离职
台风“玛娃”致广东多地暴雨 广州深圳等多市停课
制鞋机器人问世！8小时能制造600双耐克鞋
试飞危险吗？C919首飞机长这样说
陕西彬县(塌陷)发生3.2级地震 震源深度0千米
欲入中国籍替征战奥运 这位华裔美女闪亮全运赛场
中国首个火星模拟基地总体方案敲定 总投资逾4亿元
多个城市暂停投放共享单车 摩拜与ofo回应
教师因"鸡汤文"成网红:从不崇拜所谓的高考状元
飓风"哈维"导致美国得州近30万居民断电 暂无伤亡
警惕！骗子盯上共享单车 通过假冒客服平台诈骗
台湾年轻人对台失去信心转赴大陆：大陆才是未来
呼和浩特街头现大量神翻译店名
农业部回应食物农药残留
农业部回应：欧洲“毒鸡蛋”未进入中国内地市场
日战机对华紧急起飞数激增 4架战机对1架中国飞机
全国将建2442公里红色旅游公路
NHK自揭731细菌战暴行：首指日本医学界之罪
大熊猫国家公园正式获批 总面积达27134平方公里
76集团军特战部队在高原展开陆空联合演习
江西挖出巨型阴沉木
```

#### 添加日期参数

日期格式为 `YYYYMMDD`，如 20171122

```python
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
```

输出结果：

```
http://news.baidu.com/n?m=rddata&v=hot_word&type=2&date=20160705  
海南最牛副局长被双开
婚姻登记下月起免费
 记者访中央机关食堂
高铁要调价了
男子抓巨大"土豪金"鱼
河南挖出500年前古墓
大老虎自曝与女星情史
南京南站男子被卡身亡
香港将迎首位女特首
女子让儿子停课晒太阳
济南公安下属企业放贷
女镇长拍写真走红
24省下月同日省考
厅长欲掏2亿买副省长
中介为卖房和客户结婚
东北最牛大学停飞机
上海虹口体育场火灾
济南最牛钉子户被拆
复旦大学实验室爆炸
日本最美女大学生
北京未来15年规划
女子无钱打车报警
起底聊城讨债团队
韩称遭中国网络攻击
山东现国内最大金矿
最牛妈妈两胎生五子
护士怒怼医托
3名中国人在菲遭绑架
白洋淀搬迁每亩补6万
习近平会见美国国务卿
```

#### 按关键词抓取新闻

基本url为 [http://news.baidu.com/ns?tn=news](http://news.baidu.com/ns?tn=news)，接参数word字段。

```python
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
```

输出结果：

```bson
{"标题": "香港将迎首位女特首:出身贫寒 曾因考第四名痛哭一晚}_《参考消息...", "链接": "http://news.163.com/17/0327/17/CGI6I4RV00018AOQ.html", "来源": "网易", "发布日期": "2017年03月27日"}
{"标题": "香港将迎来首位女特首:出身贫寒 曾批“占中”", "链接": "http://news.china.com/domestic/945/20170327/30360029.html", "来源": "中华网", "发布日期": "2017年03月27日"}
{"标题": "香港首位女特首被评\"实干派\" 曾批\"占中\"乱港", "链接": "http://news.163.com/17/0326/22/CGG4QMGM0001875N.html", "来源": "网易", "发布日期": "2017年03月26日"}
{"标题": "香港或迎首位女特首 林郑月娥长子剑桥毕业小米任职", "链接": "http://www.donews.com/news/detail/4/2949453.html", "来源": "DoNews", "发布日期": "2017年03月26日"}
{"标题": "香港将迎来首位女特首 林郑月娥对港独态度强硬", "链接": "http://www.cnbzol.com/news/20170327114934.htm", "来源": "巴中在线", "发布日期": "2017年03月27日"}
{"标题": "香港将迎首位女特首 林郑月娥个人简历资料照片(图)", "链接": "http://www.mnw.cn/news/china/1645293-2.html", "来源": "闽南网", "发布日期": "2017年03月27日"}
{"标题": "香港迎首位女特首", "链接": "http://www.shuyang.tv/news/china/2017-03-27/208931.html", "来源": "沭阳网", "发布日期": "2017年03月27日"}
{"标题": "香港迎来首位女特首林郑月娥:寒门中苦读 作风果断民望高", "链接": "http://n.cztv.com/news/12468870.html", "来源": "新蓝网", "发布日期": "2017年03月26日"}
{"标题": "香港回归20年来将有首位女特首", "链接": "http://news.sina.com.cn/o/2017-03-27/060433853302.shtml", "来源": "新浪新闻", "发布日期": "2017年03月27日"}
{"标题": "她是香港回归以来首位女特首 将加强市民对特区政府的信任作为施政...", "链接": "http://news.163.com/17/0702/00/COA3HA1B00018AOP.html", "来源": "网易", "发布日期": "2017年07月02日"}
```
