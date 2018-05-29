import wx
import codecs
import os
import sys
sys.path.append("..")
import file_op

class PayFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(PayFrame, self).__init__(*args, **kw, size=(600,400))

        self.pnl = wx.Panel(self)
        self.make_main_ui()
        self.makeMenuBar()
        self.CreateStatusBar()
        self.SetStatusText("欢迎来到python世界!")

    def make_main_ui(self):
        # 遍历以data开头的txt文件（以后这个是要改的），展示所有程序员push代码的记录。
        upperFolder = os.path.abspath(os.path.join(os.getcwd(), ".."))
        index_line = 0
        cost_money = 0
        for filename in os.listdir(upperFolder):
            if os.path.isfile(upperFolder + '\\' + filename) and 'data' in filename:
                f = codecs.open(upperFolder + '\\' + filename, 'r',
                                encoding=file_op.get_encoding(upperFolder + '\\' + filename))
                f.seek(0)
                fl = f.readlines()
                # 遍历文件里每一条记录。
                for index in range(len(fl)):
                    cost_money += self.create_ui_line(filename, fl[index], index_line)
                    index_line += 1
                left_money = 10000 - cost_money

        st = wx.StaticText(self.pnl, label="奖池剩余奖金：" + str(left_money), pos=(25, 25))

        font = st.GetFont()
        font.PointSize += 10
        st.SetFont(font)

    def create_ui_line(self, filename, line, line_number):

        arr_line = line.split(',')

        label = filename + "\t" + arr_line[0] + "\t" + arr_line[1] + "\t" + arr_line[2] + "\t" + arr_line[3]
        wx.StaticText(self.pnl, label=label, pos=(30, 60 + line_number * 40), size=(350, 60))

        # bug: 为什么data_master.txt第1行判断为False
        if arr_line[4] == '0':
            btn = wx.Button(self.pnl, label='点击付款', pos=(500, 50 + line_number * 40), size=(60, 30), name=label)
            btn.Bind(event=wx.EVT_BUTTON, handler=self.OnPay)
            return 0
        else:
            wx.StaticText(self.pnl, label='已付款' + arr_line[3] + '元', pos=(500, 50 + line_number * 40), size=(60, 30))
            return int(arr_line[3])


    def makeMenuBar(self):
        fileMenu = wx.Menu()
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H","Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        self.Close(True)

    def OnHello(self, event):
        wx.MessageBox("Hello again wxPython")

    def OnAbout(self, event):
        wx.MessageBox("This is a wxPython Hello World sample!","About Hello World 2", wx.OK|wx.ICON_INFORMATION)

    def OnPay(self, event):
        line = event.EventObject.GetName()
        arr_line = line.split("\t")

        filename = arr_line[0]
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
                file_lines[index] = '{},{},{},{},{}\n'.format(l[0], l[1], l[2], l[3], 1)

        # 写入文件
        file = open("../" + filename, 'w', encoding='utf8')
        file.writelines(file_lines)
        file.flush()
        # 不关闭，就不能读
        file.close()

        wx.MessageBox("支付状态修改成功！")
        self.pnl.Refresh()
        self.make_main_ui()




if __name__ == '__main__':
    app = wx.App()
    frm = PayFrame(None, title='支付小工具')
    frm.Show()
    app.MainLoop()