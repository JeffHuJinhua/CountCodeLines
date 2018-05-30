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
import wx
import file_op
import socket


################### 主程序开始 ###########################
step = 0
sum = 0
hostname = socket.gethostname()
print('hostname:' + hostname)
while True: # 使用while True: 循环和 time 库实现简单的程序后台服务
    # count代表所有代码行数
    code_total = 0
    if len(sys.argv) == 1:
        path = os.getcwd()
        code_total = file_op.countcode(path)
    else:
        for path in sys.argv[1:]:
            if os.path.exists(path):
                code_total = code_total + file_op.countcode(path)
            elif path == '-h' or path == '/h':
                print('Usage: count_code_lines [directory name, [...]]')
                exit(1)
            else:
                print('The Directory ' + path +' do not exist.')
                exit(2)
    print('所有代码行数为：' + str(code_total))
    # 在windows平台下，使用系统的记事本以UTF-8编码格式存储了一个文本文件，
    # 但是由于Microsoft开发记事本的团队使用了一个非常怪异的行为来保存UTF-8编码的文件，
    # 它们自作聪明地在每个文件开头添加了0xefbbbf（十六进制）的字符，
    # 所以我们就会遇到很多不可思议的问题，比如，网页第一行可能会显示一个“？”，
    # 明明正确的程序一编译就报出语法错误，等等。
    # 可以使用 Sublime Text 编辑器-文件-保存编码-utf-8

    file_name_curr_user = 'data_' + hostname + '.txt'
    file_exist = os.path.exists(file_name_curr_user)

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    if file_exist:
        print('用户' + hostname + ' ' + file_name_curr_user + '文件存在。')
        print('遍历所有data_*.txt文件, 计算工作者提交的代码总量。')
        code_txt_total = 0
        for filename in os.listdir(os.getcwd()):
            if os.path.isfile(os.getcwd() + '\\' + filename) and 'data' in filename:
                f = codecs.open(filename, 'r', encoding=file_op.get_encoding(filename))
                f.seek(0)
                fl = f.readlines()
                s = fl[-1]
                l = s.split(',')
                lastcodeline = l[3]
                code_txt_total += int(lastcodeline)

        print('txt贡献代码行数为:' + str(code_txt_total))
        step = code_total - code_txt_total
        print('自己贡献的代码行数为:' + str(step))
        print('=' * 50)
        print('You have coded {} rows codes.'.format(step))
        print('=' * 50)

        file = codecs.open(file_name_curr_user, 'r', encoding=file_op.get_encoding(file_name_curr_user))
        file.seek(0)
        file_lines = file.readlines()
        l = file_lines[-1].split(',')
        lastyear = l[0]
        lastmonth = l[1]
        lastday = l[2]


        if year == int(lastyear) and month == int(lastmonth) and day == int(lastday):
            file_lines[-1] = '{},{},{},{},{}\n'.format(year, month, day, int(file_lines[-1].split(',')[3]) + step, 0)
            print('# in the modify')
        else:
            file_lines.append('{},{},{},{},{}\n'.format(year, month, day, step, 0))
            print('# in the append')
        for s in file_lines:
            print(s, end='')
        file = open(file_name_curr_user, 'w', encoding='utf8')
        file.writelines(file_lines)
    else:
        print('用户' + hostname + '第一次fork，创建' + file_name_curr_user + '文件,写入' + '{},{},{},{},{}\n'.format(year, month, day, 0, 0))
        file = open(file_name_curr_user, 'w', encoding='utf8')
        file.write('{},{},{},{},{}\n'.format(year, month, day, 0, 0))

    file.flush()
    # 不关闭，就不能读
    file.close()

    if step > 0:
        print('自己贡献了' + str(step) + '行代码,发送给自己的微信。')
        wx.send_wx_msg('You have coded '+ str(step) +' rows codes.', '')

    time.sleep(10)