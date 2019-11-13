"""
author:      zxzh
time:       2019.11.05
description:
"""
import os
import requests
import parsel
import pdfkit

import merge_pdf

html5_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
{content}
</body>
</html>
"""


def get_one_page_html(url):
    """
    获取网页所有内容的html代码,
    爬取的方式是get(),而非加密传输的post()
    :param url: 需要爬取的网页
    :return: response.text 返回整个网页的html代码
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        print('爬取成功')
        return response.text
    except requests.exceptions.HTTPError:
        print('遭遇反爬,请进一步处理')
        return ''


"""
函数get_menu中的chapter_info的格式
chapter_info =
[
    {
        'chapter':'parent_chapter',
        'url':'www.xxx.com',
        'child_chapters':[
        {
            'chapter':'child_chapter'
            'url':'www.xxx.com'
        }
        ]
    }
]
"""


def get_menu(prefix_url):
    """
    获取主页目录和文章标题
    :param prefix_url:目录页网址,同时也是目录跳转的前缀
    :return:返回目录信息表chapter_info和文章标题headline
    """
    html = get_one_page_html(prefix_url)  # 得到首页(目录页)html代码
    sel = parsel.Selector(html)  # 产生一个列表
    headline = sel.css('h1::text').get().replace('/', '').replace('*', '')  # 标题中有'/'和'*'会保存失败,因而去除
    chapters = sel.css('div.toctree-wrapper>ul>li').getall()  # https://readthedocs.org/统一的主页目录
    # chapters = sel.css('#python-cookbook-3rd-edition-documentation>div>ul>li').getall()  # 选择主页的目录,不指定左边的
    # 目录(反正两者只是放在html里的位置不同,指向相同,而左边的目录还要跳转多次)
    # css()选择器的get()方法是
    # 获取首次匹配的标签内容(不会获取更深层次的匹配和同级匹配)(即获取
    # 目标标签里的第一级子标签,不会进一步获取更深层次的子标签),返回匹配列表.
    # getall()方法是获取目标标签里所有代码以及所有同级目标标签的代码,
    # 包括延伸至更深层次的子标签.同样返回匹配列表,即还可以再用css()选择器
    chapter_info = []
    for chapter in chapters:  # 将html代码按行遍历,遍历根目录
        # 获取一级标题和进入详情页的url
        # print(chapter)
        ch = parsel.Selector(str(chapter))  # 每个根目录用选择器解析一下,以便选择
        postfix_url = ch.css('li.toctree-l1>a::attr(href)').get()
        # print(ch.css('li>a::attr(href)').get())  # ::text为标签间的内容,::attr(href)为熟悉值
        info = {}
        info['chapter'] = ch.css('li.toctree-l1>a::text').get().replace('/', '').replace('*', '')
        info['url'] = prefix_url + postfix_url
        # print(info['url'])

        info['child_chapters'] = []  # info字典的child_chapters的键用列表来存值
        # 获取二级标题和进入详情页的url
        if ch.css('ul') is not None:  # 如果存在子目录(ul开头),则进行提取子目录
            child_chapters = ch.css('li.toctree-l2>a').getall()  # 与根目录取法类似,
            # 都是处理好数据后再将数据添加给列表,而根目录要等这些都做完后才算处理好数据
            for child in child_chapters:
                child_sel = parsel.Selector(str(child))
                child_postfix_url = child_sel.css('a::attr(href)').get()
                #  若子目录的child_postfix_url链接里有'#',
                #  表明是网页内内容链接,那么就不需要保存
                if '#' not in child_postfix_url:
                    info['child_chapters'].append({
                        'chapter': child_sel.css('a::text').get().replace('/', '').replace('*', ''),
                        'url': prefix_url + child_postfix_url,
                    })
        chapter_info.append(info)
    return chapter_info, headline


def get_content(url):
    """
    解析网页html代码,获取目标数据
    :param url: 需要解析的网页网址
    :return: 返回网页文字主体内容部分,不同网页
    可能需要css选择器选择不同的标签,css选择器也是调试点
    """
    html = get_one_page_html(url)
    sel = parsel.Selector(html)
    content = sel.css('div.document').get()  # https://readthedocs.org/的统一文章内容定位
    # content = sel.css('[itemprop=articleBody]').get()  # itemprop="articleBody"
    content_html = html5_template.format(content=content)  # 提取出来的内容放入html5网页框架中,即格式化、美化
    return content_html


def html_to_pdf(html_str, pdf_name):
    """
    将html代码串转换成单个pdf文件,内含文件保存功能
    :param html_str: 需要转化的html代码串
    :param pdf_name: 转换成功的pdf文件,pdf_name是
    已经经过文件打开和关闭保存的实体文件
    :return: None
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': 'utf-8',
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }
    config = pdfkit.configuration(wkhtmltopdf='E:/wk Html To X/wkhtmltopdf/bin/wkhtmltopdf.exe')  # 转换工具
    # pdfkit.from_string(html_str, pdf_name, options=options)
    pdfkit.from_string(html_str, pdf_name, configuration=config)  # 将html代码串转化成pdf文件


def save_file(chapter_list):
    """
    保存文件,仅根据上文获取的二级目录及以下
    目录操作,不可操作三级及以上的章节(如有需要,自行更改)
    :param chapter_list:根据获取的文章章节列表(chapter_list)来确定保存的文件夹
    :return: None
    """
    try:
        print('开始保存')
        num = 0  # 给文件夹添加前缀字母chr(num),以便文件按顺序查看,也可以用rjust(3, str(0))右对齐(以0填充,3为总宽度)
        for chapters in chapter_list:
            url = chapters['url']
            chapter_name = chapters['chapter']
            num += 1
            dir_name = os.path.join(os.path.dirname(__file__), 'generation_file_1', f'{num}'.rjust(3, str(0)) + '-' + chapter_name)  # 在本路径(相对)下创
            # 建一个generation_file文件夹存文件,每个一级章节各有一个分路径.chr(num)是获取ascii码
            # os.path.dirname()就是获取括号内路径的目录(去掉路径的'/'后的最后一项).
            # os.path.dirname(__file__)指的是当前可执行文件所在目录
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)  # 创建分支路径,是mkdir的进阶版
            html = get_content(url)
            # print(html)
            road = os.path.join(dir_name, chapter_name + '.pdf')
            print(road)
            html_to_pdf(html, road)
            print('已保存章节' + chapter_name)

            children = chapters['child_chapters']
            if children:
                for child in children:
                    child_url = child['url']
                    child_name = child['chapter']
                    child_html = get_content(child_url)
                    html_to_pdf(child_html, os.path.join(dir_name, child_name + '.pdf'))
                    print('已保存章节' + child_name)
        print('保存完毕')
    except Exception as e:
        print('保存失败,失败原因如下:')
        print(e)


if __name__ == '__main__':
    # base_url = "https://python3-cookbook.readthedocs.io/zh_CN/latest/"
    base_url = 'https://www.runoob.com/manual/pythontutorial3/docs/html/'
    # print(get_one_page_html(base_url))
    Chapter, Headline = get_menu(base_url)
    save_file(Chapter)
    # print(Chapter)
    # print(Headline)
    merge_pdf.merge_pdf(Chapter, Headline)
