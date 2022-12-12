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

if __name__ == '__main__':
    # 连接 namenode
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")
    filename = 'x.txt'
    # 获取允许的分块大小
    blocksize = c.getBlockSize()
    # blocksize = 1024
    # 将文件分块 得到块数
    blocknum = splitBySize(filename , blocksize)

    # 拿到各块存储位置
    location = c.getLocation(filename , blocknum)
    print(location)

    # 向目的地址传送文件块
    path = "./output"
    files = os.listdir(path)
    for i in range(blocknum):
        fp = open(os.path.join(path, files[i]), 'rb')
        [filename, extname] = os.path.splitext(files[i])
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
                newloc = c.changeIP(filename, i + 1, j)
                print("changeed ip: " + newloc[0] + "\n")
                # ftp.set_debuglevel(2)
                ftp.connect(newloc[0], 21)
                ftp.login("ftpuser", "ftppass")
                filename = str(newloc[1]) + extname
                ftp.storbinary('STOR /' + filename, fp, 1024)
                ftp.close()
