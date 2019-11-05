"""
name:         main.py  为主函数
author :     zxzh
time :       2019.11.03
suggestion: 调试建议,根据爬取的网址拿到请
            求头headers和cookie,网页内容
            的具体提取与处理在clear_html.py
            中,更改它就行了
description : transform Html of CSDN to PDF file，
            将CSDN的文章保存为PDF文件，注意cookies
            的实效性,headers和cookies都在目标网页
            按F12的开发者工具里的network里
"""
# 引入系统库和第三方库

# 引入自定义的文件
import get_html
import save_file
import transform_file
import clear_html
import html_template


# 全局变量
url = "https://www.bilibili.com/read/cv3280065"  # 爬取网址
root_menu = "E:/Python/zxzhexercise/HtmlToPDF/file/"  # 用来指定文件存储根目录

# 请求头
headers = {
"Host":"www.bilibili.com",
"Referer":"https://space.bilibili.com/356758350/favlist?fid=articles",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}
# 用户信息(cookie有时效性,但可以搭建cookie词，
# 可以实时维护.其他方法会消耗电脑大量性能)
cookie = {
    "Cookie": "_uuid=E4A4D658-B7D1-8CE2-D9B5-7217CC43EEAC39005infoc; LIVE_BUVID=AUTO4615419250395553; sid=jg4or38b; fts=1541943409; buvid3=033E20A3-C309-4827-948C-6542981B6F6928874infoc; CURRENT_FNVAL=16; im_notify_type_356758350=0; PHPSESSID=cj86qelt6iqe184ihvlakg0b95; _ga=GA1.2.2014666213.1545890733; stardustvideo=1; stardustpgcv=0606; rpdid=|(JlRmJYk||R0J'ullY|uR)kY; UM_distinctid=16aba9c254bd0-00b9d2c43d2c5d-3c604504-100200-16aba9c254c1a1; im_seqno_356758350=8; im_local_unread_356758350=0; _uuid=6A3DB01B-4186-2DAD-E82C-6EEDA2E2E44258845infoc; INTVER=1; __guid=104670726.3775872268332355600.1567934838970.1804; laboratory=1-1; route=; CURRENT_QUALITY=80; bp_t_offset_27555844=316474046734336964; DedeUserID=356758350; DedeUserID__ckMd5=e9194b2226231a35; SESSDATA=1ca63125%2C1575121518%2Ca17cf6a1; bili_jct=817b6b9e53925f2075a94d3e84f3c7af; finger=edc6ecda; bp_t_offset_356758350=317313635533079257; monitor_count=146"
}


if __name__ == '__main__':
    text1 = get_html.get_html_text(url, headers, cookie)
    clear_code, title = clear_html.clear_html(text1, html_template.html_template)
    print(clear_code)
    book_name = save_file.save_html(clear_code, root_menu, title)
    transform_file.html_to_pdf(book_name)
