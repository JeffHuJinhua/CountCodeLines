'''
V8.180516: 发送微信消息
V7.180515: 发送微信消息2
v6.180510: 文件记录数据
v5.180509: 代码增量实现
v4.180508: 后台服务实现
v3.180508: 命令行参数实现
v2.180508: 函数递归实现
v1.180507: 复用函数实现
v0.180507: 流程语句实现
'''

import sys
import os
import time
import datetime
import codecs
import wx_op
import file_op



################### 主程序开始 ###########################
step = 0
sum = 0

while True: # 使用while True: 循环和 time 库实现简单的程序后台服务
    count = 0
    if len(sys.argv) == 1:
        path = os.getcwd()
        count = file_op.count_code(path)
    else:
        for path in sys.argv[1:]:
            if os.path.exists(path):
                count = count + file_op.count_code(path)
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

    f = codecs.open('data.txt', 'r', encoding=file_op.get_encoding('data.txt'))
    f.seek(0)
    fl = f.readlines()
    s = fl[-1]
    #print(s)

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
    print('step=' + str(step))
    if step > 0:
        wx_op.send_wx_msg('You have coded ' + str(step) + ' rows codes.', '')

    time.sleep(10)



