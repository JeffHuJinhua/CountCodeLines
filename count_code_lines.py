'''
V8.180516: ����΢����Ϣ
V7.180515: ����΢����Ϣ2
v6.180510: �ļ���¼����
v5.180509: ��������ʵ��
v4.180508: ��̨����ʵ��
v3.180508: �����в���ʵ��
v2.180508: �����ݹ�ʵ��
v1.180507: ���ú���ʵ��
v0.180507: �������ʵ��
'''

import os
import sys
import time
import datetime
import itchat

def countcode(path):
    i = 0   # �ݹ���������У��������������붨���λ�ò��ԣ�ʵ���߼��ͻ����
    pathList = os.listdir(path)
    for filename in pathList:
        if os.path.isfile(path + '\\' + filename):
            if filename.endswith('.py'):    # �� endswith() ���� in ����ȷƥ�䣬�����ȡ�� .pyc �ļ�ʱ�ı��뱨������
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

    return i    # �ݹ���������У�return ���ڴӺ����ڲ����ݷ���ֵ������λ�þ����ݹ麯���ķ��ؽ�����

def send_wx_msg(msg, nickname): #msg: ���͵���Ϣ nickName: ΢���ǳ�
    itchat.auto_login(hotReload=True) # ΢�ŵ�¼
    users = itchat.search_friends(name=nickname) #����΢���û�
    itchat.send(msg, users[0]['UserName'])  #UserNameΪ΢�źţ���һ���ܳ�����ĸ


################### ������ʼ ###########################
step = 0
sum = 0

while True: # ʹ��while True: ѭ���� time ��ʵ�ּ򵥵ĳ����̨����
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

    # ��windowsƽ̨�£�ʹ��ϵͳ�ļ��±���UTF-8�����ʽ�洢��һ���ı��ļ���
    # ��������Microsoft�������±����Ŷ�ʹ����һ���ǳ��������Ϊ������UTF-8������ļ���
    # ����������������ÿ���ļ���ͷ�����0xefbbbf��ʮ�����ƣ����ַ���
    # �������Ǿͻ������ܶ಻��˼������⣬���磬��ҳ��һ�п��ܻ���ʾһ����������
    # ������ȷ�ĳ���һ����ͱ����﷨���󣬵ȵȡ�
    # ����ʹ�� Sublime Text �༭��-�ļ�-�������-utf-8

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

    if step != 0:
        send_wx_msg('You have coded '+ str(step) +' rows codes.', '���B')


    time.sleep(10)



