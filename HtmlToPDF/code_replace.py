import os


# 这里的文件打开与关闭是为了创造可按行读取的代码,
# 这个办法非常蠢,其实查找替换用正则表达式的sub就行了
def code_replace(code, older, newer):
    with open('mid.txt', 'w', encoding='utf-8') as f_mid:
        f_mid.write(code)
        f_mid.close()
    with open('mid.txt', 'r', encoding='utf-8') as f_mid1:
        mid_read_list = f_mid1.readlines()
        f_mid1.close()
    #  保存替换后的代码
    f = open('mid.txt', 'w', encoding='utf-8')
    for number_row in mid_read_list:
        f.write(number_row.replace(older, newer))  # 每一行找到目标进行替换
    f.close()
    with open('mid.txt', 'r', encoding='utf-8') as f2:
        code1 = f2.read()  # 使用read而不是readlines()返回的不是列表
    f2.close()
    os.remove('mid.txt')
    return code1

