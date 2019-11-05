"""
author:      zxzh
time:       2019.11.05
description:利用选择器找到需要的内容,
            利用正则表达式进行批量替
            换无法显示图片的代码使其
            可显示
"""
import re
import parsel


def clear_html(text, html_template):
    """
    提取网页主体部分,丢弃广告等部分
    :param text: 输入参数是html代码
    :param html_template:html代码的结构模板
    :return: 返回第一个参数净化后的代码replace_code;返回第二个参数为文章标题
    """
    sel = parsel.Selector(text)  # 将request.get()获得的字符串转换成可以选择的结构

    article = sel.css('div.article-holder').get()  # bilibili的文章内容在
    # <div class="article-holder"></div>里之前用浏览器直接copy selector时,多了一些其他的导致没有成功
    title = sel.css('h1::text').get()

    # article = sel.css('article').get()  # css选择器(标签选择器)进行选取,这里
    # 的article是CSDN的html网页代码文章主体部分标签.文章只有一个article,所以指明提取article
    # title = sel.css('h1.article-title::text').get()  # 提取文章的标题(位于h1标签的文本text中)

    html = html_template.format(article=article)  # 转换成html格式,
    # 将选择器得到的article填到html_template中{article}占位的地方
    """
    本代码找到了如何替换网页img标签中的 data-src为src(使用正则表达式的sub方法),很多网页的
    图片调用使用的是data-src,因而下载时网页内容图片无法下载
    """
    # 通过正则表达式的替换函数将图片源的data-src换成src,并添加网址的HTTP协议头
    replace_code = re.sub('data-src=\"//', 'src=\"https://', html)
    # print(replace_code)
    return replace_code, title
