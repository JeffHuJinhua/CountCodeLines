import chardet
import os
import codecs


def count_code(path):
    i = 0   # 递归迭代函数中，函数级变量代码定义的位置不对，实现逻辑就会出错
    path_list = os.listdir(path)
    for filename in path_list:
        if os.path.isfile(path + '/' + filename):
            if filename.endswith('.py'):    # 用 endswith() 代替 in ，精确匹配，解决读取到 .pyc 文件时的编码报错问题
                print(filename + ' ' + get_encoding(path + '/' + filename))
                f = codecs.open(path + '/' + filename, encoding = get_encoding(path + '/' + filename))
                k = 0
                for line in f.readlines():
                    line = line.strip()
                    if not line.startswith('#') and len(line):
                        k += 1
                i += k
                print(str(k) + '行')

        if os.path.isdir(path + '/' + filename):
            current_path = path + '/' + filename
            j = count_code(current_path)
            if j:
                i = i + j

    return i    # 递归迭代函数中，return 用于从函数内部传递返回值出来；位置决定递归函数的返回结束！


def count_newline(path):
    i = 0   # 递归迭代函数中，函数级变量代码定义的位置不对，实现逻辑就会出错
    path_list = os.listdir(path)

    for filename in path_list:
        if os.path.isfile(path + '/' + filename):
            if filename.endswith('.py'):    # 用 endswith() 代替 in ，精确匹配，解决读取到 .pyc 文件时的编码报错问题
                print(filename + ' ' + get_encoding(path + '/' + filename))
                f = codecs.open(path + '/' + filename, encoding = get_encoding(path + '/' + filename))
                k = 0
                for line in f.readlines():
                    line = line.strip()
                    if not len(line):
                        k += 1
                i += k
                print(str(k) + '行')
        if os.path.isdir(path + '/' + filename):
            current_path = path + '/' + filename
            j = count_newline(current_path)
            if j:
                i = i + j
    return i    # 递归迭代函数中，return 用于从函数内部传递返回值出来；位置决定递归函数的返回结束！


def count_comment(path):
    i = 0   # 递归迭代函数中，函数级变量代码定义的位置不对，实现逻辑就会出错
    path_list = os.listdir(path)
    print("计算Comment行数")
    for filename in path_list:
        if os.path.isfile(path + '/' + filename):
            if filename.endswith('.py'):    # 用 endswith() 代替 in ，精确匹配，解决读取到 .pyc 文件时的编码报错问题
                print(filename + ' ' + get_encoding(path + '/' + filename))
                f = codecs.open(path + '/' + filename, encoding = get_encoding(path + '/' + filename))
                k = 0
                for line in f.readlines():
                    line = line.strip()
                    if line.startswith('#'):
                        k += 1
                i += k

                print(str(k) + '行')
        if os.path.isdir(path + '/' + filename):
            current_path = path + '/' + filename
            j = count_comment(current_path)
            if j:
                i = i + j
    return i    # 递归迭代函数中，return 用于从函数内部传递返回值出来；位置决定递归函数的返回结束！


def count_all(path):
    i = 0   # 递归迭代函数中，函数级变量代码定义的位置不对，实现逻辑就会出错
    path_list = os.listdir(path)
    for filename in path_list:
        if os.path.isfile(path + '/' + filename):
            if filename.endswith('.py'):    # 用 endswith() 代替 in ，精确匹配，解决读取到 .pyc 文件时的编码报错问题
                print(filename + ' ' + get_encoding(path + '/' + filename))
                f = codecs.open(path + '/' + filename, encoding = get_encoding(path + '/' + filename))
                k = len(f.readlines())
                print(str(k) + '行')
                i += k
        if os.path.isdir(path + '/' + filename):
            current_path = path + '/' + filename
            j = count_all(current_path)
            if j:
                i = i + j

    return i    # 递归迭代函数中，return 用于从函数内部传递返回值出来；位置决定递归函数的返回结束！


def get_encoding(file):
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']


def find_last_line_index(lines):
    for index in range(len(lines)-1, -1, -1):
        if len(lines[index].strip()) == 0:
            continue
        else:
            return index

def count_code_line_txt(path):
    code_sum = 0
    for filename in os.listdir(path):
        if os.path.isfile(path + '/' + filename) and 'data' in filename:
            f = codecs.open(path + '/' + filename, 'r',
                            encoding=get_encoding(path + '/' + filename))
            f.seek(0)
            fl = f.readlines()
            # 遍历文件里每一条记录。
            for index in range(len(fl)):
                if len(fl[index].strip()) == 0:
                    continue;
                code_sum += int(fl[index].split(',')[5])
    return code_sum
