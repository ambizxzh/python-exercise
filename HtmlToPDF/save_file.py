"""
author:      zxzh
time:       2019.11.05
description:判断文件路径、和文件是否存在,
            不存在则新建,存在则让使用者
            选择是否删除以便重新保存
"""

import os


def save_html(text, root_menu, title):
    """
    保存html内容
    :param text: html代码,request响应体的text格式内容,而非content格式
    :param root_menu:保存文件的路径
    :param title:文章标题
    :return:返回保存的html文件的文件名file_name
    """
    if not os.path.exists(root_menu):  # 如果没有根目录，那么就建一个目录
        os.mkdir(root_menu)
    # html, title = clear_html.clear_html(text, html_template.html_template)
    file_name = root_menu + f'{title}.html'  # 这里的f'{}'是格式化字符串,与str.format(),print("%d")这两种同种类
    if not os.path.exists(file_name):  # 如果这个文件名没有存在，那么开始爬取网页信息
        with open(file_name, mode='w', encoding='utf-8') as f:  # 保存为utf-8格式的文件
            f.write(text)
            f.close()
            print("文件保存成功！")
            return file_name
    else:
        print("文件已存在！")
        value = input("是否删除已存在文件,删除则输入1,输入其他任意数字将退出转换:")
        print(value)
        if value == str(1):
            os.remove(file_name)
            if os.path.exists(file_name.strip('.html') + '.pdf'):
                os.remove(file_name.strip('.html') + '.pdf')
            print("删除成功")
            if not os.path.exists(file_name):  # 如果这个文件名没有存在，那么开始爬取网页信息
                with open(file_name, mode='w', encoding='utf-8') as f:  # 保存为utf-8格式的文件
                    f.write(text)
                    f.close()
                    print("文件重新保存成功！")
        return file_name
