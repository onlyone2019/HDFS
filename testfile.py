# import zerorpc
#
# class main(object):
#     def __init__(self):
#         # 根节点 "/"
#         self.root = "wangjie1234134"
#     def hello(self , name):
#         return self.root
#
# s = zerorpc.Server(main())
# s.bind("tcp://0.0.0.0:4242")
# s.run()

'''
s = '/'
s = s.split('/')
print(s)
for x in s:
    if x == "":
        s.remove(x)
s = "/".join(s)
print(s)
'''

from ftplib import FTP

ftp=FTP()          		      #设置变量 ，实例化
ftp.set_debuglevel(2)         #打开调试级别2，显示详细信息
ftp.connect("192.168.0.168",21)      #连接的ftp sever和端口
# ftp.login("user","password")  #连接的用户名，密码
print(ftp.getwelcome())