"""
author:      zxzh
time:       2019.11.14
description: 下载图片,这些图片是静态存储在网页链接里
"""
import os
import pysnooper
import parsel
import requests


def download_one_page(url):
    """
    获取一页网页,这里是一个生成器(使用了yield),提取网页中需要的信息
    :param url: 需要获取的网页
    :return: 用yield返回一个生成器序列 [src, title]
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        sel = parsel.Selector(html)
        images = sel.css('img.ui.image.lazy')  # 由于需要二次提取,因而不使用get()方法将内容提取出来,而是保留选择器的类型以便二次提取
        # 二次提取
        for img in images:
            src = img.css('img::attr(data-original)').get()
            title = img.css('img::attr(alt)').get()
            # 一个带有 yield 的函数就是一个 generator(生成器),
            # 它和普通函数不同,生成一个generator看起来像函数调用,
            # 但不会执行任何函数代码,直到对其调用 next()
            # (在for循环中会自动调用next())才开始执行.
            # 虽然执行流程仍按函数的流程执行,但每执行到一个yield语句
            # 就会中断,并返回一个迭代值,下次执行时从 yield 的下一个语句继续执行.
            # 看起来就好像一个函数在正常执行的过程中被 yield 中断了数次，
            # 每次中断都会通过 yield 返回当前的迭代值。
            yield src, title
    except Exception as e:
        print('爬取网页错误,错误如下:')
        print(e)


@pysnooper.snoop()
def save_image(gene):
    """
    使用生成器的标题命名文件(图片文件名)来保存生成器获取到的内容(图片)
    :param gene: 生成器序列
    :return: None
    """
    try:
        response = requests.get(gene[0])
        response.raise_for_status()
        if not os.path.exists('image_download'):
            os.mkdir('image_download')
        file_name = os.path.join(os.path.dirname(__file__), 'image_download',
                                 gene[1] + '.' + gene[0].split('.')[-1])
        with open(file_name, 'wb') as f:
            f.write(response.content)  # content是字节的,而text是html的字符串形式,是content处理后得到的
            f.close()
    except Exception as e:
        print('爬取图片内容错误,错误代码如下:')
        print(e)


if __name__ == '__main__':
    for num in range(1, 11):
        base_url = f'https://www.fabiaoqing.com/bqb/lists/page/{num}.html'
        # 产生生成器,只有调用next()方法(for循环自带这个方法)时才执行生成器函数里的代码
        generator = download_one_page(base_url)
        for gen in generator:
            save_image(gen)
