"""
author:      zxzh
time:       2019.11.05
description: 通过文件夹列表或者章节列表将pdf进行合并
"""
import os
import shutil
from PyPDF2 import PdfFileReader, PdfFileWriter


def merge_pdf(storage_path, output_pdf_name):
    """
    将多个PDF文件合并成一个,并删除原文件
    :param storage_path: 存储路径列表,其实就是爬取的章节列表
    :param output_pdf_name: 合并后的PDF的文件名
    :return: None
    """
    page_number = 0
    pdf_output = PdfFileWriter()
    mid_num = 0  # 和保存那边是匹配的,都使用chr(mid_num)产生字母,以便pycharm识别文件顺序
    for pdf in storage_path:
        primary_chapter = pdf['chapter']
        mid_num += 1
        dir_name = os.path.join(os.path.dirname(
            __file__), 'generation_file_1', f'{mid_num}'.rjust(3, str(0)) + '-' + primary_chapter)  # 文件夹路径

        read_path = os.path.join(
            dir_name, primary_chapter + '.pdf')  # 文件路径
        pdf_input = PdfFileReader(open(read_path, 'rb'))
        # 获取PDF页数
        page_count = pdf_input.getNumPages()
        for page in range(page_count):  # 按页读,读一页写一页
            pdf_output.addPage(pdf_input.getPage(page))

        # 添加书签
        parent_bookmark = pdf_output.addBookmark(primary_chapter, page_number)
        # 更新标签页码
        page_number += page_count

        # 存在子章节时
        if pdf['child_chapters']:
            for child_chapter in pdf['child_chapters']:
                second_level_directory = child_chapter['chapter']
                child_path = os.path.join(
                    dir_name, second_level_directory + '.pdf')
                pdf_input = PdfFileReader(open(child_path, 'rb'))
                # 获取页数
                page_count = pdf_input.getNumPages()
                # 按页写
                for page in range(page_count):
                    pdf_output.addPage(pdf_input.getPage(page))

                # 添加标签
                pdf_output.addBookmark(second_level_directory, pagenum=page_number
                                       , parent=parent_bookmark)
                # 更新标签页码
                page_number += page_count
    # 合并PDF
    pdf_output.write(open(output_pdf_name + '.pdf', 'wb'))

    # 无法自动删除文件,因为用PyPDF2无法关闭打开的文件
    # 删除所有原文件(将文件夹目录(这里删除了generation目录)删除,为官方标准库)
    # if eval(input('是否删除所有子文件,只保留合并文件 (输入1则删除,输入其他数字则不删除):')) == 1:
    #     shutil.rmtree(os.path.join(os.path.dirname(__file__), 'generation_file'))
    #     print('删除成功')
    return ''


def merge_through_path(path_list, output_name):
    page_num = 0
    write_buf = PdfFileWriter()  # 重命名函数,增加可读性
    for path_deliver in path_list:  # 取出每个文件夹
        if path_deliver['child_files']:  # 若文件有子文件

            parent_mark = None
            if not len(path_deliver['child_files']) == 1:  # 若子文件不止一个
                folder = path_deliver['folder'] + '.pdf'
                # folders 子文件名
                folders = folder.strip(folder.split('-')[0]).strip('-')
                folder_path = os.path.join(path_deliver['directories'], folders)
                # 这个if语句的内容和下面存储子文件的内容一样,只是说这个文件与章节目录有关就分出来了
                if folders in path_deliver['child_files']:  # 若文件夹中包含与文件夹名相同的文件
                    read = PdfFileReader(open(folder_path, 'rb'))
                    page_count = read.getNumPages()
                    for pag in range(page_count):
                        write_buf.addPage(read.getPage(pag))
                    parent_mark = write_buf.addBookmark(folders.strip('.pdf'), pagenum=page_num)
                    path_deliver['child_files'].remove(folders)  # 从文件列表中移除这个文件,以免重复
                    page_num += page_count
                # else:
                #     # 利用写方法来添加书签path_deliver['folder'],父标签,在上一并列标签的末尾
                #     parent_mark = write_buf.addBookmark(path_deliver['folder'], pagenum=page_num-1)

            for file in path_deliver['child_files']:  # 取出每个子文件,逐步添加到合并的文件中
                # 取得文件路径,式中dirname(__file__)是为了排除运行路径的影响
                file_root = os.path.join(os.path.dirname(__file__), path_deliver['directories'], file)
                read_buf = PdfFileReader(open(file_root, 'rb'))  # 重命名函数,增加可读性
                # write_buf = PdfFileWriter()  # 这个要全局变量,重命名函数,增加可读性
                page_count = read_buf.getNumPages()  # 读取页数
                for page in range(page_count):  # 从原文件逐页读写到合并的文件中
                    write_buf.addPage(read_buf.getPage(page))

                book_mark = write_buf.addBookmark(file.strip('.pdf'), pagenum=page_num, parent=parent_mark)  # 利用写方法来添加书签
                PdfFileReader(open(file_root, 'rb'))
                page_num += page_count  # 更新标签页码
                print('将' + file + '写入缓冲区完毕')

    write_buf.write(open(output_name + '.pdf', 'wb'))  # 将所有在缓冲区的内容写入合并的文件夹
    print('合并成功')
    # 无法自动删除文件,因为用PyPDF2无法关闭打开的文件
    # if eval(input('是否删除所有子文件,只保留合并文件 (输入1则删除,输入其他数字则不删除):')) == 1:
    #     shutil.rmtree(os.path.join(os.path.dirname(__file__), path_list[0]['folder']))
    #     print('删除了' + path_list[0]['folder'])
    return ''
