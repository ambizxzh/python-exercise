"""
author:      zxzh
time:       2019.11.05
description:利用request库爬取网页代码
"""
import requests


def get_html_text(url, headers, cookie):
    """
    获取html的text
    :param url:需要爬取的网址
    :param headers:爬取网址的请求头,解决反爬
    :param cookie:爬取网址的有实效的cookie协议码,解决反爬
    :return:正确爬取则返回爬取的html代码(response.text),否则返回空
    """
    try:
        # 发送一个请求(网址),url是网址,返回响应体
        response = requests.get(url, headers=headers, cookies=cookie)
        response.raise_for_status()  # 爬取的网页连接状态,如果连接不
        # 是200状态,产生一个HttpError的异常,并跳到except
        response.encoding = response.apparent_encoding  # 将utf-8(apparent_encoding)
        # 的编码给网页编码(encoding)
        print("爬取成功")
        # print(response.text)
        return response.text
    except:
        print("爬取失败！")
        return ''

