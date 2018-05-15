'''
V7.180515: 发送微信消息
v6.180510: 文件记录数据
v5.180509: 代码增量实现
v4.180508: 后台服务实现
v3.180508: 命令行参数实现
v2.180508: 函数递归实现
v1.180507: 复用函数实现
v0.180507: 流程语句实现
'''

import os
import sys
import time
import datetime

def countcode(path):
    i = 0   # 递归迭代函数中，函数级变量代码定义的位置不对，实现逻辑就会出错
    pathList = os.listdir(path)
    for filename in pathList:
        if os.path.isfile(path + '\\' + filename):
            if filename.endswith('.py'):    # 用 endswith() 代替 in ，精确匹配，解决读取到 .pyc 文件时的编码报错问题
                f = open(path + '\\' + filename, encoding = 'utf8')
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


step = 0
sum = 0

while True: # 使用while True: 循环和 time 库实现简单的程序后台服务
    count = 0
    if len(sys.argv) == 1:
        path = os.getcwd()
        count = countcode(path)
    else:
        for path in sys.argv[1:]:
            if os.path.exists(path):
                count = count + countcode(path)
            elif path == '-h' or path == '/h':
                print('Usage: count_code_lines [directory name, [...]]')
                exit(1)
            else:
                print('The Directory ' + path +' do not exist.')
                exit(2)

    # 在windows平台下，使用系统的记事本以UTF-8编码格式存储了一个文本文件，
    # 但是由于Microsoft开发记事本的团队使用了一个非常怪异的行为来保存UTF-8编码的文件，
    # 它们自作聪明地在每个文件开头添加了0xefbbbf（十六进制）的字符，
    # 所以我们就会遇到很多不可思议的问题，比如，网页第一行可能会显示一个“？”，
    # 明明正确的程序一编译就报出语法错误，等等。
    # 可以使用 Sublime Text 编辑器-文件-保存编码-utf-8

    f = open('data.txt', 'r', encoding='utf8')
    f.seek(0)
    fl = f.readlines()
    s = fl[-1]
    print(s)

    l = s.split(',')
    lastyear = l[0]
    lastmonth = l[1]
    lastday = l[2]
    lastcodeline = l[3]

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    count0 = int(lastcodeline)

    print('count = ' + str(count) + '\n')
    step = count - count0
    count0 = count
    sum = sum + step

    print('=' * 50)
    print('You have coded {} rows codes.'.format(sum))
    print('=' * 50)

    print(str(day) + '|' + lastday + '|' + str(sum))
    if year == int(lastyear) and month == int(lastmonth) and day == int(lastday):
        fl[-1] = '{},{},{},{}\n'.format(year,month,day,sum)
        print('# in the modify')
    else:
        fl.append('{},{},{},{}\n'.format(year,month,day,sum))
        print('# in the append')
    for s in fl:
        print(s, end='')
    f = open('data.txt', 'w', encoding='utf8')
    f.writelines(fl)
    f.flush()

    time.sleep(10)