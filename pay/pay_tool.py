import wx
import codecs
import os
import sys
sys.path.append("..")
import file_op


class PayFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(PayFrame, self).__init__(*args, **kw, size=(1000,500))

        self.pnl = wx.Panel(self)
        self.make_main_ui()
        self.make_menu_bar()
        self.CreateStatusBar()
        self.SetStatusText("欢迎来到python世界!")

    def make_main_ui(self):
        # 遍历以data开头的txt文件（以后这个是要改的），展示所有程序员push代码的记录。
        upper_folder = os.path.abspath(os.path.join(os.getcwd(), ".."))
        index_line = 0
        cost_money = 0
        print(upper_folder)
        wx.StaticText(self.pnl, label="成员\t\t\t\t年\t\t月\t\t日\t\t空白行\t\t注释行\t\t代码行\t\t是否付款", pos=(30, 80), size=(850, 30))
        for filename in os.listdir(upper_folder):
            if os.path.isfile(upper_folder + '\\' + filename) and 'data' in filename:
                f = codecs.open(upper_folder + '\\' + filename, 'r',
                                encoding=file_op.get_encoding(upper_folder + '\\' + filename))
                f.seek(0)
                fl = f.readlines()
                # 遍历文件里每一条记录。
                for index in range(len(fl)):
                    if len(fl[index].strip()) == 0:
                        continue;
                    cost_money += self.create_ui_line(filename, fl[index], index_line)
                    index_line += 1
                left_money = 10000 - cost_money

        st = wx.StaticText(self.pnl, label="奖池剩余奖金：" + str(left_money), pos=(25, 25))

        font = st.GetFont()
        font.PointSize += 10
        st.SetFont(font)

    def create_ui_line(self, filename, line, line_number):
        print('create_ui_line:' + line)
        arr_line = line.split(',')
        dev_name = filename.replace("data_","").replace(".txt", "")
        label = dev_name + "\t" + arr_line[0] + "\t" + arr_line[1] + "\t" + arr_line[2] + "\t" + arr_line[3]

        wx.StaticText(self.pnl, label=dev_name, pos=(30, 120 + line_number * 40), size=(130, 60))
        wx.StaticText(self.pnl, label=arr_line[0], pos=(200, 120 + line_number * 40), size=(100, 60))
        wx.StaticText(self.pnl, label=arr_line[1], pos=(300, 120 + line_number * 40), size=(100, 60))
        wx.StaticText(self.pnl, label=arr_line[2], pos=(400, 120 + line_number * 40), size=(100, 60))
        wx.StaticText(self.pnl, label=arr_line[3], pos=(500, 120 + line_number * 40), size=(100, 60))
        wx.StaticText(self.pnl, label=arr_line[4], pos=(600, 120 + line_number * 40), size=(100, 60))
        wx.StaticText(self.pnl, label=arr_line[5], pos=(700, 120 + line_number * 40), size=(100, 60))

        # 最后一列有\t\n,所有取值是要去掉。
        if arr_line[6][0] == '0':
            btn = wx.Button(self.pnl, label='点击付款', pos=(800, 110 + line_number * 40), size=(80, 30), name=label)
            btn.Bind(event=wx.EVT_BUTTON, handler=self.on_pay)
            return 0
        else:
            wx.StaticText(self.pnl, label='已付款' + arr_line[5] + '元', pos=(800, 120 + line_number * 40), size=(80, 30))
            return int(arr_line[5])

    def make_menu_bar(self):
        file_menu = wx.Menu()
        hello_item = file_menu.Append(-1, "&Hello...\tCtrl-H","Help string shown in status bar for this menu item")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT)
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT)
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.on_hello, hello_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)

    def on_exit(self, event):
        self.Close(True)

    def on_hello(self, event):
        wx.MessageBox("Hello again wxPython")

    def on_about(self, event):
        wx.MessageBox("This is a wxPython Hello World sample!", "About Hello World 2", wx.OK | wx.ICON_INFORMATION)

    def on_pay(self, event):
        line = event.EventObject.GetName()
        arr_line = line.split("\t")

        filename = 'data_' + arr_line[0] + '.txt'
        year = arr_line[1]
        month = arr_line[2]
        day = arr_line[3]

        file = codecs.open("../" + filename, 'r', encoding=file_op.get_encoding("../" + filename))
        file.seek(0)
        file_lines = file.readlines()
        # 根据当前点击这行的年月日去确定修改文件的哪一行。

        for index in range(len(file_lines)):
            l = file_lines[index].split(',')
            if l[0] == year and l[1] == month and l[2] == day:
                file_lines[index] = '{},{},{},{},{},{},{}\n'.format(l[0], l[1], l[2], l[3], l[4], l[5], 1)

        # 写入文件
        file = open("../" + filename, 'w', encoding='utf8')
        file.writelines(file_lines)
        file.flush()
        # 不关闭，就不能读
        file.close()

        wx.MessageBox("支付状态修改成功！")

        self.Destroy()
        frm = PayFrame(None, title='支付小工具')
        frm.Show()

if __name__ == '__main__':
    app = wx.App()
    frm = PayFrame(None, title='支付小工具')
    frm.Show()
    app.MainLoop()