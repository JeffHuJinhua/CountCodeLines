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
import socket
import git

################### 主程序开始 ###########################
push_code = 0
sum = 0
hostname = socket.gethostname()
# mac会出现两个hostname，一个正确的，还有一个加local的。修复：去掉local
print('代码行数计数程序开始===> ')
print('程序员主机名:' + hostname)
if '.local' in hostname:
    print('程序员mac电脑的hostname包含.local字符, 去掉.local处理。')
    hostname = hostname.replace('.local', '')

git_base_path = os.path.abspath(os.path.join(os.getcwd(), "../../.."))
print("git_base_path:" + git_base_path)
while True: # 使用while True: 循环和 time 库实现简单的程序后台服务
    code_total = 0
    comment_total = 0
    newline_total = 0
    if len(sys.argv) == 1:
        code_total = file_op.count_code(git_base_path)
        comment_total = file_op.count_comment(git_base_path)
        newline_total = file_op.count_newline(git_base_path)
    else:
        for path in sys.argv[1:]:
            if os.path.exists(path):
                code_total = code_total + file_op.count_code(path)
                comment_total += file_op.count_comment(path)
                newline_total += file_op.count_newline(path)
                #all_total += file_op.count_all(path)
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

    file_name_curr_user = git_base_path + '/' + hostname + '.ccl'
    file_exist = os.path.exists(file_name_curr_user)

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    if not file_exist:
        print('程序员count文件不存在，创建文件。' + file_name_curr_user)
        file = open(file_name_curr_user, 'w', encoding='utf8')
        file.close()

    print('遍历所有*.ccl文件, 计算工作者提交的代码总量。')
    code_txt_total = 0
    newline_txt_total = 0
    comment_txt_total = 0
    for filename in os.listdir(git_base_path):
        filename = git_base_path + '/' + filename
        if os.path.isfile(filename) and filename.endswith('.ccl'):
            print('处理文件：' + filename)
            f = codecs.open(filename, 'r', encoding=file_op.get_encoding(filename))
            f.seek(0)

            file_lines = f.readlines()
            for line in file_lines:
                if len(line.strip()) == 0:
                    continue
                col = line.split(',')
                newline_txt_total += int(col[3])
                comment_txt_total += int(col[4])
                code_txt_total += int(col[5])

    print('txt贡献代码行数为:' + str(code_txt_total))
    push_code = code_total - code_txt_total
    push_newline = newline_total - newline_txt_total
    push_comment = comment_total - comment_txt_total
    print('自己贡献的代码行数为:' + str(push_code))
    print('=' * 50)
    print('You have coded {} rows codes.'.format(push_code))
    print('=' * 50)

    file = codecs.open(file_name_curr_user, 'r', encoding=file_op.get_encoding(file_name_curr_user))
    file.seek(0)
    file_lines = file.readlines();

    lastyear = 0
    lastmonth = 0
    lastday = 0
    old_push_code = 0
    old_push_newline = 0
    old_push_comment = 0
    pay_status = 0
    if len(file_lines) > 0:
        print('文件'+file_name_curr_user+'为空')
        index_last_line = file_op.find_last_line_index(file_lines)
        col = file_lines[index_last_line].split(',')
        lastyear = col[0]
        lastmonth = col[1]
        lastday = col[2]
        old_push_code = int(col[5])
        old_push_newline = int(col[3])
        old_push_comment = int(col[4])
        pay_status = col[6]

    if year == int(lastyear) and month == int(lastmonth) and day == int(lastday):
        file_lines[index_last_line] = '{},{},{},{},{},{},{}'.format(
            year, month, day, old_push_newline + push_newline, old_push_comment + push_comment, old_push_code + push_code, pay_status)
        print('# in the modify')
    else:
        file_lines.append('{},{},{},{},{},{},{}\n'.format(year, month, day, push_newline, push_comment, push_code, 0))
        print('# in the append')

    print(str(file_lines))
    file = open(file_name_curr_user, 'w', encoding='utf8')
    file.writelines(file_lines)

    file.flush()
    # 不关闭，就不能读
    file.close()

    #if step > 0:
    #    print('自己贡献了' + str(step) + '行代码,发送给自己的微信。')
    #    wx_op.send_wx_msg('You have coded ' + str(step) + ' rows codes.', '')

    # 自动add程序员的count文件
    repo = git.Repo(git_base_path)
    repo.git.add(file_name_curr_user)

    #time.sleep(100000)
    break
