import itchat

def send_wx_msg(msg, nickname): #msg: 发送的消息 nickName: 微信昵称
    itchat.auto_login(hotReload=True) # 微信登录
    users = itchat.search_friends(name=nickname) #查找微信用户
    itchat.send(msg, users[0]['UserName'])  #UserName为微信号，是一串很长的字母