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