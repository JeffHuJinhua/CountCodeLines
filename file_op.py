import chardet
import os
import codecs


def countcode(path):
    i = 0   # 递归迭代函数中，函数级变量代码定义的位置不对，实现逻辑就会出错
    path_list = os.listdir(path)
    for filename in path_list:
        if os.path.isfile(path + '\\' + filename):
            if filename.endswith('.py'):    # 用 endswith() 代替 in ，精确匹配，解决读取到 .pyc 文件时的编码报错问题
                print(get_encoding(path + '\\' + filename))
                f = codecs.open(path + '\\' + filename, encoding = get_encoding(path + '\\' + filename))
                s = f.readline()
                k = 0
                while s:
                    k = k + 1
                    s = f.readline()
                i = i + k

                print(path + '\\' + filename + ': ' + str(k))
        if os.path.isdir(path + '\\' + filename):
            currentPath = path + '\\' + filename
            j = countcode(currentPath)
            if j:
                i = i + j

    return i    # 递归迭代函数中，return 用于从函数内部传递返回值出来；位置决定递归函数的返回结束！


def get_encoding(file):
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']
