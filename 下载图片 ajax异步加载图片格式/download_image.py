"""
Encoding: 'utf-8'
Author:    zxzh
Times:     2019.11.14
Description:下载花瓣网(https://huaban.com/)的图片,
在这个花瓣主页键入搜索关键词,打开的网页的ajax异步加载将具有规律性
"""
import os
import requests
import parsel
import jsonpath  # 用来提取json格式
from urllib.request import urlretrieve  # 快速下载
"""
ajax异步加载:请求的资源发生变化,但是地址栏的url没有变化
实际上它发生了一些反应 ,把资源都储存在了中间件中 ,当我们将网页向下滑动时 ,网页会在中间件请求资源
因此达到了在不重新加载整个网页的前提下 ,资源发生变化, 监听这个网路请求, 可以看到它访问的中间件是谁
没有出现中间件以前是网页资源变化 则url必定会变化
"""
"""
抓包方法 : 在需要爬取的网页页面  按 F12 --> Network栏  --> XHR栏 --> Name栏 --> 
-->向下滑动网页,观察到Name栏发生变化,这些就是被抓取的包 --> 点击其中一个包 -->使用preview栏查看
每一个包都有 Headers,Preview,Response,Cookies,Timing
Headers:请求头,爬取时需要提供的请求
Preview:是抓包获得的Html格式的响应体,与完整的网页源代码有区别,是Response的格式化(可阅读性)
Response:上面已经提过
Cookies:在Headers里有
Timing:时间相关

F12的得到的开发者工具有栏目 Elements,Console,Source,Network,Application等
# 详情可去该网址看看https://blog.csdn.net/Andy2019/article/details/80632335
Elements:是网页源代码Html
Console:是开发者使用的命令行工具
Source:用于断点调试js,内容和Elements一样
Network:从发起网页页面请求Request后分析HTTP请求后得到的各个请求资源信息（包括状态、资源类型、大小、所用时间等）
对于响应体(request.get()或request.post()获取到的)
.text是以文本格式取Elements中的全部,即网页源代码
.json()是json格式取网页源代码
"""


def get_one_page(url, head=None):
    try:
        req = requests.get(url, headers=head)  # 获取json,只要"X-Requested-With": "XMLHttpRequest"存在就一定是请求json格式,
        # 无论响应体调用什么方法,返回的一定是json格式,如req.text也是json格式
        # 之前在使用json()方法时出现 expecting value: 1 line 1 column,
        # 是因为没有加请求头,网上的一些关于此错误的也是差不多,只是说网上的是分开给get()的参数赋值的如params=params,headers=headers

        req2 = requests.get(url)  # 获取网页
        return req.json(), req2.text
    except Exception as e:
        print('访问出错,错误如下')
        print(e)


def download_picture(jso, htm=None, search=None):
    # sel = parsel.Selector(htm)
    # img_prefix_url = sel.css('img::attr(src)').get()
    try:
        # jsonpath()选择器返回的是列表类型
        # jsonpath()使用方法见网址 https://www.cnblogs.com/angle6-liu/p/10580792.html
        img_suffix_urls = jsonpath.jsonpath(jso, '$..file.key')
        file_ids = jsonpath.jsonpath(jso, '$..file_id')
        file_types = jsonpath.jsonpath(jso, '$..file.type')
        if not os.path.exists('picture' + '/' + f'{search}'):
            os.mkdir('picture' + '/' + f'{search}')
        # 解压操作,for循环对列表的遍历其实就是解压,多重遍历解压就是让他们一一对应.
        # zip的作用就是让多个列表同时遍历,使之一一对应
        numb = 0  # 记录每页保存图片的数目
        for file_id, file_type, img_suffix_url in zip(file_ids, file_types, img_suffix_urls):
            file_path = os.path.join(os.path.dirname(__file__), 'picture', f'{search}',
                                     str(file_id) + '.' + file_type.split('/')[-1])
            img_url = img_prefix_url + img_suffix_url
            urlretrieve(img_url, file_path)  # 专门用来下载,与下面注释的作用一样
            numb += 1
            # file_path = os.path.join(os.path.dirname(__file__), 'picture',
            #                          str(file_id) + '.' + file_type.split('/')[-1])
            # req = requests.get(img_prefix_url + img_suffix_url)
            # with open(file_path, 'wb') as f:
            #     f.write(req.content)
        return numb
    except Exception as e:
        print('保存出错,错误如下')
        print(e)


if __name__ == '__main__':
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        # "Cookie": "referer=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DCOHWbxPkxlKbpZcz9P3GvCJ08mxMjkRfFm2Pc1KST2u%26wd%3D%26eqid%3D8af7e53d00008606000000025dc97241; __guid=170314297.3555241462739402000.1573483090834.9463; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAABJElEQVRYR%2B1VOxYCIQwMF7KzsvFGXmW9kY2VnQfxCvgCRmfzCD9lnz53myWQAJOZBEfeeyIi7xz%2FyEXzZRPFhYbPc3hHXO6I6TbFixmfEyByeQQSxu6BcAXSkIGMazMjuBcz8pQcq44o0Iuyyc1p38C62kNsOdeSZDOQlLRQ80uOMalDgWCGMfsW2B5%2FATMUyGh2uhgptV9Ly6l5nNOa1%2F6zmjTqkH2aGEk2jY72%2B5k%2BNd9lBfLMh8GIP11iK95vw8uv7RQr4oNxOfbQ%2F7g5Z4meveyt0uKDEIiMLRC4jrG1%2FjkwKxCRE2e5lF30leyXYvQ628MZKV3q64HUFvnPAMkVuSWlEouLSiuV6dp2WtPBrPZ7uO5I18tbXWvEC27t%2BTcv%2Bx0JuJAoUm2L%2FQAAAABJRU5ErkJggg%3D%3D%2CWin32.1366.768.24; _uab_collina=157348309151329593871297; UM_distinctid=16e5ae6978b2a6-0985f0a4d34347-3c604504-100200-16e5ae6978cd8; __auc=d4144b7016e5ae69abb357f38a9; _hmt=1; sid=cN0yb26b5ZfuYcJrKvQ5rHLdNUl.GlV4g0kHdX6Wdo8gfh8JSQK0Xz4c5MNqpwBuKp1zt8A; BAIDU_SSP_lcr=https://www.baidu.com/link?url=4JnByaW4tWQ5DSwTB1pRDJzWrO54K9vEdPznfpv0zpW&wd=&eqid=d3464afc004ca445000000065dccb908; __gads=ID=48a2ba3ec02995bb:T=1573700610:S=ALNI_MaaAwndQo0e5AhY_3toathBirL3OQ; Hm_lvt_d4a0e7c3cd16eb58a65472f40e7ee543=1573483092,1573697852,1573709008,1573709027; CNZZDATA1256903590=1231655239-1573480106-https%253A%252F%252Fwww.baidu.com%252F%7C1573720050; __asc=1a5f6dfa16e691050e40518572d; monitor_count=28; Hm_lpvt_d4a0e7c3cd16eb58a65472f40e7ee543=1573722832; _cnzz_CV1256903590=is-logon%7Clogged-out%7C1573722833324",
        "Host": "huaban.com",
        "Referer": "https://huaban.com/explore/donghuadianyinghaibao",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "X-Request": "JSON",
        "X-Requested-With": "XMLHttpRequest",
    }
    for num in range(1, 11):
        # search_word = '鬼刀'
        # base_url = f'https://huaban.com/search/?q=%E9%AC%BC%E5%88%80&k2ytuz1n&page={num}&per_page=20&wfl=1'  # 鬼刀

        search_word = 'Pixiv'  # 搜索关键词,用来给分文件命名以及利用关键词搜索 打开的网页抓包以便后续程序循环执行
        base_url = f'https://huaban.com/search/?q=Pixiv&k2ytshml&page={num}&per_page=20&wfl=1'  # pixiv
        # 这个异步在请求头里,是搜索框键入关键字才会有规律可循(page=数字)

        img_prefix_url = 'http://hbimg.huabanimg.com/'  # 在Elements的<img></>标签中的图片源有这个前缀,也可以用代码获取
        jsons, html = get_one_page(base_url, headers)
        files = download_picture(jsons, html, search_word)
        print('第{}页下载了完成了{}张图片'.format(num, files))

