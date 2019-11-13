"""
author:      zxzh
time:       2019.11.05
description:获取文件夹的所有子文件夹和子文件,
            返回一个列表
"""
import os
import sys

import pysnooper  # 第三方库,用于监听程序运行过程,类似于日志,便于调试
import shutil
# 自写库
import merge_pdf


def traverse_directory(dir2, file_name=[], directory=[], dir_list=[]):
    """
    递归函数,根据dir2的变化作为递归依据,
    其他几个列表作为递归时不丢失的存储空间
    :param dir2:文件夹路径
    :param file_name: 递归遍历到的 所有文件名的 列表
    :param directory: 递归遍历到的 所有文件夹名的 列表
    :param dir_list: 递归遍历的得到的"每一级目录"
    及 "目录里的所有文件和文件夹" 等构成的字典 保存在列表里
    :return:返回遍历的三个列表,主要起存储每次遍历的数据,
    使其不丢失,并且不用全局变量存储
    """
    # 自调用递归获得文件夹的所有文件列表和路径列表
    new_dir = dir2
    if os.path.isfile(dir2):
        # file_path.append(dir2)  # 文件路径列表
        file_name.append(os.path.basename(dir2))  # 文件名列表
    elif os.path.isdir(dir2):
        directory.append(os.path.basename(dir2))
        for s in os.listdir(dir2):  # listdir()方法是列出文件夹里的子文件夹和文件名
            new_dir = os.path.join(dir2, s)
            traverse_directory(new_dir)
        dir_list.append(
            {
                'folder': os.path.basename(dir2),  # 当前文件夹名
                'directories': dir2,  # 当前所在目录(路径)
                'child_files&folders': os.listdir(dir2)  # 当前文件夹所有的一级文件夹和文件
            }
        )
    return directory, file_name, dir_list


@pysnooper.snoop()
def traverse_directory_super(dir1, extension=''):  # 与普通版的区别在于字典里多了些参数,以及列表首项是输入的目录文件夹(普通版该项在尾部)
    """
    对输入的文件夹进行遍历,输出一个储存字典的数组
    :param dir1: 需要遍历的文件夹
    :param extension: 文件扩展名,用指定特定的文件类型,默认为空,即没有扩展名要求
    :return: 返回一个储存字典的数组
    """
    dir_list = []
    for root, dirs, files in os.walk(dir1):  # os.walk是一个生成器,需要不断遍历它
        # 每次遍历都返回一个三元组(root, dirs, files)
        # root : 当前正在遍历的文件夹(不是它的子文件夹)地址
        # dirs : 是一个list,是当前文件夹中所有目录的名字(不包含子目录)
        # files : 是一个list,是当前文件夹中所有文件的名字(不包含子目录)
        dir_list.append(
            {
                'folder': os.path.basename(root),  # 当前文件夹名
                'directories': root,  # 当前文件夹所在目录
                'child_folders': dirs,  # 当前文件的所有一级子文件夹
                'child_files': [fi for fi in files if fi.endswith(extension)],  # 当前目录下的一级所有(扩展名为extension)的子文件,即不含子目录里的
                'child_files&folders': os.listdir(root)  # 当前目录下的所有一级子文件和文件夹,不含子目录
            }
        )
    return dir_list


if __name__ == '__main__':
    # xx, yy, zz = traverse_directory("E:/Python/zxzhexercise/爬取网页转成PDF/python3-cookbook craw/generation_file")
    # print(xx)
    print('++++++++++++++++++++++++++++')
    # print(zz)
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    # print(yy)
    lst = traverse_directory_super("F:/python/网络爬虫与信息提取", extension='.pdf')
    # print(lst)
    # merge_pdf.merge_through_path(lst, 'E:/Python/zxzhexercise/爬取网页转成PDF/python3-cookbook craw/合并')
    merge_pdf.merge_through_path(lst, "F:/python/网络爬虫与信息提取/爬虫课程合集")
