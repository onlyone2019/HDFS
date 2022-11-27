from ftplib import FTP
import zerorpc
import os

size = 1024

def merge(dir , name):
    files = os.listdir(dir)
    print(files)
    target = "./merge/" + name
    for file in files:
        file = dir + file
        with open(file, 'rb') as fin:
            with open(target ,'ab') as fout:
                buf = fin.read(1024)
                while len(buf) > 0:
                    fout.write(buf)
                    buf = fin.read(size)

if __name__ == '__main__':
    # 连接 namenode
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    # 拿到文件存储位置信息
    path = "/x.txt"
    location = c.get(path)
    # location = [['192.168.0.168', 2], ['192.168.0.168', 4], ['192.168.0.168', 6]]
    print("location ")
    print(location)

    [_, extname] = os.path.splitext(path) #获取后缀名
    print("extname " + extname)
    for loc in location:
        filename = loc[0] + "_" + str(loc[1]) + extname
        print("filename " + filename)
        remotefilename = str(loc[1]) + extname
        ftp = FTP()
        ftp.set_debuglevel(2)
        ftp.connect(loc[0], 21)
        ftp.login("ftpuser", "ftppass")
        file_handle = open("./fileFromDatanode/" + filename, "wb").write
        ftp.retrbinary("RETR " + remotefilename, file_handle, size)
        ftp.close()
    merge("./fileFromDatanode/" , "x.txt")


