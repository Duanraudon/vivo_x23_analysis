# 关于vivo x23的八千条评论分析

如今的时代是数据的时代，采集数据和分析数据对企业显得尤为重要。而对于我们个人而言，运用数据进行理性抉择也是一个不错的选择。这次我分析了有关于vivo x23的八千多条评论，首先数据是从vivo官网商城，淘宝，京东的商品评论中获取，采用的工具是Python的requests库。接着运用matplotlib，SnowNLP，wordcloud等库对采集的数据进行数据分析，由此完成了这整个的一个项目。


## 工具
- Python3.6.5
- Google Chrome浏览器
- Pycharm

## 目录
- 数据采集与清洗
- 评论数据展示
- 数据分析
- 评论分析展示

## 数据采集与清洗

​        用Google Chrome浏览器的开发者工具分析vivo官网，京东，淘宝的评论，发现这三个网站的共同点都是运用的json来显示数据，于是我分别提取了他们的网址，之后获取到数据信息提取我们想要的评论，接着把获取到的评论存储到文本文件中，最后进行数据的清洗工作，去除多余的空格和无用的评论。

```python
import requests
import json
from lxml import etree

class get_alldatas(object):
    #淘宝七家店铺和京东两家还有vivo官网商城的json评论网址
    def __init__(self):
        self.taobao_urls_list = [
            'https://rate.tmall.com/list_detail_rate.htm?itemId=575602013665&sellerId=883737303&currentPage=',
            'https://rate.tmall.com/list_detail_rate.htm?itemId=575446668300&sellerId=2616970884&currentPage=',
            'https://rate.tmall.com/list_detail_rate.htm?itemId=575743333423&sellerId=1999920158&currentPage=',
            'https://rate.tmall.com/list_detail_rate.htm?itemId=575579308869&sellerId=1637289231&currentPage=',
            'https://rate.tmall.com/list_detail_rate.htm?itemId=575580236569&sellerId=1687434761&currentPage=',
            'https://rate.tmall.com/list_detail_rate.htm?itemId=575749197781&sellerId=707928640&currentPage=',
            'https://rate.tmall.com/list_detail_rate.htm?itemId=575982975316&sellerId=1864868535&currentPage=',
            ]
        self.jingdong_urls_list = [
            'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv393&productId=31461047265&score=0&sortType=5&page=',
            'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv37&productId=100000469124&score=0&sortType=5&page=',
        ]
        self.vivo_official_urls_list = 'http://shop.vivo.com.cn/product/remark?prodId=10486&onlyHasPicture=false&fullpaySkuIdSet=5424%2C5425&pageNum='
    #淘宝，vivo官网商城网页源码解析
    def get_HtmlText(self,url):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.content.decode('utf-8')
        except:
            return ''
    #京东源码解析
    def get_jingdongHtmlText(self,url):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return ''
    #淘宝评论提取和保存
    def taobao_urlsdata_save(self,taobao_json):
        try:
            json_data = json.loads(taobao_json.replace('jsonp128(','').strip(')'))
            datas = json_data["rateDetail"]['rateList']
            data = []
            for i in datas:
                content = i["rateContent"]
                if content:
                    data.append(content)
                    data.append("\n")
            if data:
                with open("vivo评论.txt", 'a+', encoding="utf-8") as f:
                    f.writelines(data)
                    f.write('\n')
                return 'continue'
        except:
                return 'end'
    #淘宝七家店铺网址循环采集
    def taobao_out_urls(self):
        for url in self.taobao_urls_list:
            for num in range(1, 98):
                urls = url + str(num)
                taobao_json_data = self.get_HtmlText(urls)
                data = self.taobao_urlsdata_save(taobao_json_data)
                if data != 'continue':
                    print('taobaopages{}'.format(num))
                    break
    #京东评论提取和采集
    def jingdong_urlsdata_save(self,html):
        try:
            js_data = html.replace('fetchJSON_comment98vv393(', '').replace('fetchJSON_comment98vv37(', '').strip(');')
            comment = json.loads(js_data)
            comment = comment['comments']
            data = []
            for i in comment:
                content = i['content']
                data.append(content)
                data.append("\n")
            if data:
                with open('vivo评论.txt', 'a+', encoding="utf-8") as f:
                    f.writelines(data)
                    f.write('\n')
                return 'continue'
        except:
            return 'end'
    #京东两家店铺网址循环
    def jingdong_out_urls(self):
        for url in self.jingdong_urls_list:
            for num in range(1, 1000):
                urls = url + str(num) + '&pageSize=10&isShadowSku=0&rid=0&fold=1'
                jingdong_json_data = self.get_jingdongHtmlText(urls)
                data = self.jingdong_urlsdata_save(jingdong_json_data)
                if data != 'continue':
                    print('jingdongpages{}'.format(num))
                    break
    #vivo官网商城评论提取和保存
    def vivo_official_urldatas_save(self, html):
        try:
            html = etree.HTML(html)
            data = html.xpath('//li[@class="evaluate"]/p/text()')
            datas = []
            for i in list(data):
                datas.append(i)
                datas.append('\n')
            if data:
                with open('vivo评论.txt', 'a+', encoding='utf-8') as f:
                    f.writelines(datas)
                    f.write('\n')
                return 'continue'
        except:
            return 'end'
    #vivo官网商城网址循环
    def vivo_official_out_urls(self):
        for num in range(1,500):
            url = self.vivo_official_urls_list + str(num)
            html = self.get_HtmlText(url)
            data = self.vivo_official_urldatas_save(html)
            if data != 'continue':
                print('vivo_official_pages{}'.format(num))
                break

#提取到的所有评论清洗
def dealwith_alldatas():
    file1 = open('vivo评论.txt', 'r', encoding='utf-8')
    file2 = open('vivo评论清洗.txt', 'w', encoding='utf-8')
    try:
        for line in file1.readlines():
            if  line == '\n' or line == '此用户没有填写评论!\n' or line == '此用户未填写评价内容\n':
                line = line.replace('此用户没有填写评论!\n','').replace('此用户未填写评价内容\n','')
                line = line.strip('\n')
            file2.write(line)
    finally:
        file1.close()
        file2.close()

if __name__ == "__main__":
    getalldatas = get_alldatas()
    getalldatas.taobao_out_urls()
    getalldatas.jingdong_out_urls()
    getalldatas.vivo_official_out_urls()
    dealwith_alldatas()
```

## 评论数据展示

这是得到清洗后的部分评论。

![1.png](https://upload-images.jianshu.io/upload_images/5498924-f896f56ede1a8e7b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 数据分析

这里用到了一个中文文本情感分析库SnowNLP，它可以把我们的评论逐条的进行情感分析，情感系数越接近1则代表该评论为积极态度，越接近0则表示为消极态度。将得到的所有评论的情感系数保存在csv文件中以备接下来的情感系数分布图和评论分布图的制作。在这里还用到了一个词云制作库wordcloud，它可以把我们得到的评论出现最多的字段显示为词云状态，字体越大则表示出现的频率越高。

```python
import re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from wordcloud import WordCloud
from snownlp import SnowNLP
from collections import Counter

#打开我们获取的评论文本文件进行评论情感系数处理与保存
def sentiments_file():
    s_sentiments = []
    with open(r'vivo评论清洗.txt','r',encoding='utf-8') as f:
        for i in f.readlines():
            s = SnowNLP(i)
            s_sentiments.append(s.sentiments)
    with open('sentiments.csv','w',encoding='utf-8') as w:
        w.write(str(s_sentiments).strip('[]'))
        w.close()

#词云图制作
def wordcloud_plot():
    #出现最多的字段统计，取前200
    with open(r'vivo评论清洗.txt', 'r', encoding='utf-8') as f:
        words = re.findall(r'\w+', f.read().lower())
    word_number = Counter(words)
    common = word_number.most_common(200)
    #删除不需要的字段
    del common[2]
    w = WordCloud(font_path='youyuan.TTF', 
                  background_color='white', 
                  width=750,
                  height=175, 
                  max_font_size=45)
    w.generate_from_frequencies(dict(common))
    ax = plt.subplot2grid((4,4), (0,0), rowspan=2,colspan=4)
    ax.imshow(w, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('评论词云图')

#情感系数分布图
def emotion_plot():

    b = np.loadtxt('sentiments.csv', delimiter=',', dtype=np.float64)
    ax1 = plt.subplot2grid((4,4), (2,0), rowspan=2,colspan=2)
    ax1.hist(b,
             bins=20,
             color='royalblue',
             histtype='bar',
             rwidth=0.8,)
    ax1.set_xlabel('情感系数', )
    ax1.set_ylabel('数量', )
    ax1.set_title('情感系数分布图')

#评论分布图
def comment_plot():
    b = np.loadtxt('sentiments.csv', delimiter=',', dtype=np.float64)
    good = [x for x in b if 2/3<=x<=1.0]
    medium = [x for x in b if 1/3<=x<=2/3]
    bad = [x for x in b if 0.0<=x<=1/3]
    comment_lenth = [len(x) for x in [good, medium, bad]]
    comment = [len(x)/sum(comment_lenth) for x in [good, medium, bad]]
    #颜色配置
    cmap = plt.get_cmap("tab20c")
    colors = cmap(np.arange(3))
    ax2 = plt.subplot2grid((4,4), (2,2), rowspan=2,colspan=2,)
    ax2.pie(comment,
            labels=['好评', '中评', '差评'],
            radius=0.75,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops={'width':0.45, 'edgecolor':'w'},
            pctdistance=0.7)
    ax2.axis('equal')
    ax2.set_title('评论分布图')
    plt.tight_layout()
    plt.show()

if __name__=='__main__':
    sentiments_file()
    #全局变量字体，字体大小设置
    matplotlib.rcParams['font.family']='YouYuan'
    matplotlib.rcParams['font.size']=10
    wordcloud_plot()
    emotion_plot()
    comment_plot()
```

## 评论分析展示

这是得到的词云图，情感系数分布图和评论分布图。从词云图中可以得知vivo x23的卖点在于外观的漂亮，运行的速度还有手感舒适等方面。从情感系数分布图可以观察大约有4000左右的人评论态度特别积极，有500左右的人评论态度特别消极。从评论分布图中我们可以得知vivo x23的好评占比百分之七十五，中评百分之十二，差评百分之十二。总体而言vivo x23这款手机表现的还是相当不错的。

![Figure_2.png](https://upload-images.jianshu.io/upload_images/5498924-318abeb21a2cce5a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
