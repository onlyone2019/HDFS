from ftplib import FTP
import zerorpc
import os

def mkSubFile(srcName, cnt, buf):
    [des_filename, extname] = os.path.splitext(srcName)
    filename = "./output/" + des_filename + str(cnt) + extname
    print('正在生成子文件: %s' % filename)
    with open(filename, 'wb') as fout:
        fout.write(buf)

def splitBySize(filename, size):
    with open(filename, 'rb') as fin:
        buf = fin.read(size)
        cnt = 0
        while len(buf) > 0:
            mkSubFile(filename, cnt + 1, buf)
            cnt += 1
            buf = fin.read(size)
    return cnt

def merge(dir , name , size):
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

class Client:
    def __init__(self, host):
        self.c = zerorpc.Client()
        self.c.connect(host)
        print("host  ---------")


    def mkdir(self, path):
        return self.c.mkdir(path)

    def putfile(self, path):
        # 获取允许的分块大小
        blocksize = self.c.getBlockSize()
        # blocksize = 1024
        # 将文件分块 得到块数
        blocknum = splitBySize(path, blocksize)
        # 拿到各块存储位置
        location = self.c.getLocation(path, blocknum)
        print(location)
        [filename, extname] = os.path.splitext(path.split('/')[-1])
        # 向目的地址传送文件块
        path = "./output"
        files = os.listdir(path)
        for i in range(blocknum):
            fp = open(os.path.join(path, files[i]), 'rb')
            ftp = FTP()
            for j in location[i]:
                try:
                    # ftp.set_debuglevel(2)
                    ftp.connect(j[0], 21)
                    ftp.login("ftpuser", "ftppass")
                    storefilename = filename + j[1] + extname
                    ftp.storbinary('STOR /' + storefilename, fp, 1024)
                    ftp.close()
                except:
                    newloc = self.c.changeIP(filename, i + 1, j)
                    print("changeed ip: " + newloc[0] + "\n")
                    # ftp.set_debuglevel(2)
                    ftp.connect(newloc[0], 21)
                    ftp.login("ftpuser", "ftppass")
                    filename = str(newloc[1]) + extname
                    ftp.storbinary('STOR /' + filename, fp, 1024)
                    ftp.close()

    def getfile(self, path):
        # 拿到文件存储位置信息
        path = "/x.txt"
        location = self.c.get(path)

        # 获取允许的分块大小
        blocksize = self.c.getBlockSize()

        [filename, extname] = os.path.splitext(path.split('/')[-1])

        for loc in location:
            name = loc[0] + "_" + filename + str(loc[1]) + extname
            print("name "+ name)
            remotefilename = filename + str(loc[1]) + extname
            ftp = FTP()
            # ftp.set_debuglevel(2)
            ftp.connect(loc[0], 21)
            ftp.login("ftpuser", "ftppass")
            file_handle = open("./fileFromDatanode/" + filename, "wb").write
            ftp.retrbinary("RETR " + remotefilename, file_handle, blocksize)
            ftp.close()
        merge("./fileFromDatanode/", filename+extname , blocksize)
        print("合并的文件请见：./fileFromDatanode/"+filename+extname)

    def cat(self, path):
        self.getfile(path)
        [filename, extname] = os.path.splitext(path.split('/')[-1])
        file_object = open("./fileFromDatanode/" + filename + extname, 'r', encoding='utf-8')
        for string in file_object:
            print(string)
        file_object.close()

    def ls(self, path):
        return self.c.ls(path)

    def mv(self, src, des):
        return self.c.mv(src, des)

    def cp(self, src, des):
        pass

    def rm(self, path):
        return self.c.rm(path)

if __name__ == '__main__':
    client = Client("tcp://127.0.0.1:4242")
    client.mkdir("/dir1")
    client.mkdir("/dir1/dir2")
    client.mkdir("/dir1/dir3")
    print(client.ls("/"))
    print(client.ls("/dir1"))
    print(client.rm("/dir1"))
    print(client.ls("/"))
