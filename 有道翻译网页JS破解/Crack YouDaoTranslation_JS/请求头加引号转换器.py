"""
description:给请求头加引号,需要转换的请求头
            复制到headers_string里,将打印输
            出的复制到header字典里就行
"""

import re

headers_string = """
Accept:application/json, text/javascript, */*; q=0.01
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9
Connection:keep-alive
Content-Length:251
Content-Type:application/x-www-form-urlencoded; charset=UTF-8
Cookie:JSESSIONID=abc1cit8z4HmAhH6wTDNw; _ntes_nnid=0637a8cf8806a288f7ef75db4e9581d4,1554202852975; OUTFOX_SEARCH_USER_ID_NCOO=509122527.4623523; OUTFOX_SEARCH_USER_ID=-532728416@36.157.22.18; NTES_SESS=43VeRtB3qihtRWXauj1YrtWPJEAPyvo60.hrNHMWCNfLCIEACNjlM8HWo5Kkgu7uN8NzsCghNHhpeZ4wtjKDs7XOMpZFkPFSg6GKP.MY5Z5qxGWHm0A6yWi4PBzy9vGIh5au6ChUc1PoKaYVlrI5NmTqbbvnGd6LSm1LaYQ3_mPVPr5VwzZfi5Kvt1ulnGbWXOiqlzqAhtoOBEHqiGP1.wKOG; ANTICSRF=40bc32214d5d070e0fc448f13737d55e; S_INFO=1572430904|0|3&80##|bupt888; P_INFO=bupt888@163.com|1572430904|0|other|00&99|bej&1572430784&mail_client#bej&null#10#0#0|186207&0|mail163|bupt888@163.com; DICT_UGC=24ce5af95c30b6ce68d2e8c2c34936f7|bupt888@163.com; __guid=204659719.3564575597047851500.1573032359887.8047; monitor_count=4; ___rl__test__cookies=1573032586794
Host:fanyi.youdao.com
Origin:http://fanyi.youdao.com
Referer:http://fanyi.youdao.com/
User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
X-Requested-With:XMLHttpRequest
"""


def transform(headers_str):
    pattern = '^(.*?):(.*)$'  # 请求头原有格式
    for line in headers_str.splitlines():
        print(re.sub(pattern, '\"\\1\": \"\\2\",', line))


if __name__ == "__main__":
    transform(headers_string)
