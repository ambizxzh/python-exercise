"""
description:爬取有道网页版的翻译,
            模拟人工输入得到网页
            给的翻译结果
            这是属于非常规破解,常规破解一般是破解js文件
"""
import requests
import hashlib
import time
import random


# 用户浏览器参数
appVersion = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (" \
             "KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"


def make_md5(s):
    """
    description:产生Md5码值
    :param s:
    :return:
    """
    result_md5 = hashlib.md5(s.encode())
    return str(result_md5.hexdigest())


def translation(e):
    # 对于有道这类网页动态翻译交互结果.
    # 模拟人工的一切参数所在位置在如下地方找:
    # (1)打开在有道线翻译(动态交互页)
    # (2)在页面按F12,进入开发工具里,找到Network栏
    # (3)在页面随意输入词,点击翻译.此时Network将发生动态变化
    # (4)点击动态变化的Network(同时点击下面相邻的栏的XHR)的Name框最上面的一行,
    # 右侧就有我们需要的信息:url, Request Method, Request Headers, Form Data
    # (a)url与浏览器地址栏不同,是因为Request Method为POST
    # (将网址参数(包含在url和Form Data里)放在Headers里,以密文(安全)访问)
    # (b)Form Data里面也包含了页面显示但不在网页源代码的信息,
    # 这次需要破解的信息就在这个Form Data里
    # (c)Request Headers是为反爬设计的,其中User Agent是用户信息(代表人为)
    # Cookie是实时协议码这里Cookie也重要

    # 破解(解密)步骤(对于网页出现的元素而网页源代码不出现,那么这些元素是在JS代码里)
    # 1,双击Form Data中需要破解的元素名,Ctrl+Shift+F来搜索这个元素名
    # 2,找到与这个元素有关的.js文件(若有多个文件,则换个元素关键词,因为Form Data
    # 里的元素在一个.js文件里,.js文件多是因为你的浏览器有安装浏览器插件),双击进去
    # 3,在js代码中用Ctrl+F继续查找元素名,在众多找到的匹配中,根据对比和经验找到加密的语句
    url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    ts = str(int(time.time() * 1000))  # ts是时间戳,为了与Form Data
    # 同格式乘以了1000(位数达到),int取整,再str化成字符串给字典的值
    i = ts + str(random.randint(0, 9))
    sign = "fanyideskweb" + e + i + "n%A-rKaT5fb[Gy?;N5@Tj"
    form_data = {
        "i": e,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": i,  # 时间戳加随机整数,由于是随机的,对方也不知道这个值,所以这里直接随机没关系
        "sign": make_md5(sign),
        "ts": ts,
        "bv": make_md5(appVersion),
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME",
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "251",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "JSESSIONID=abc1cit8z4HmAhH6wTDNw; _ntes_nnid=0637a8cf8806a288f7ef75db4e9581d4,1554202852975; OUTFOX_SEARCH_USER_ID_NCOO=509122527.4623523; OUTFOX_SEARCH_USER_ID=-532728416@36.157.22.18; NTES_SESS=43VeRtB3qihtRWXauj1YrtWPJEAPyvo60.hrNHMWCNfLCIEACNjlM8HWo5Kkgu7uN8NzsCghNHhpeZ4wtjKDs7XOMpZFkPFSg6GKP.MY5Z5qxGWHm0A6yWi4PBzy9vGIh5au6ChUc1PoKaYVlrI5NmTqbbvnGd6LSm1LaYQ3_mPVPr5VwzZfi5Kvt1ulnGbWXOiqlzqAhtoOBEHqiGP1.wKOG; ANTICSRF=40bc32214d5d070e0fc448f13737d55e; S_INFO=1572430904|0|3&80##|bupt888; P_INFO=bupt888@163.com|1572430904|0|other|00&99|bej&1572430784&mail_client#bej&null#10#0#0|186207&0|mail163|bupt888@163.com; DICT_UGC=24ce5af95c30b6ce68d2e8c2c34936f7|bupt888@163.com; __guid=204659719.3564575597047851500.1573032359887.8047; monitor_count=4; ___rl__test__cookies=1573032586794",
        "Host": "fanyi.youdao.com",
        "Origin": "http://fanyi.youdao.com",
        "Referer": "http://fanyi.youdao.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    response = requests.post(url, data=form_data, headers=headers)
    return response.json()  # 返回可以直接给python使用格式,不能使用text


if __name__ == '__main__':
    while 1:
        word = input("请输入需要翻译的词汇:")
        result = translation(word)
        print(result['translateResult'][0][0])
