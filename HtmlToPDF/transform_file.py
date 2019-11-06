import os
import pdfkit


def html_to_pdf(name):
    """
    将html文件转换为pdf文件
    :param name:
    :return:
    """
    if os.path.exists(name):
        if not os.path.exists(name.strip('.html') + ".pdf"):
            print("正在进行转换")
            # 找到用来转换的exe文件的路径
            config = pdfkit.configuration(wkhtmltopdf='E:/wk Html To X/wkhtmltopdf/bin/wkhtmltopdf.exe')
            pdfkit.from_file(name, name.strip('.html') + ".pdf", configuration=config)
            print("转换成功")
        else:
            print("pdf文件已存在,无需转换")
