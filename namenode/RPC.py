import zerorpc
import queue
import random
import FileClasses as FC
import os
import _pickle as pk
import atexit
import time, threading
from ftplib import FTP
import FileClasses as FC

'''
class caculate(object):
    # 查看hdfs中的目录信息
    def ls(self, path):
        return
    # 创建文件夹
    def mkdir(self, path):
        return
    # 移动文件或重命名
    def mv(self, src, target):
        return
    # 上传到HDFS中
    def put(self, file, path):
        return
    # 下载文件到客户端
    def get(self, file, path):
        return
    # 删除文件
    def rmr(self, path):
        return
    # 查看文件内容
    def cat(self, file):
        return
    # 追加文件内容
    def appendToFile(self, localfile, hdfsfile):
        return
    # 复制hdfs中的文件到另一个目录
    def cp(self, src, target):
        return
    def hello(self , name):
        return "jie"
'''

root = None

def addDirectoryToDirectory(father, mydir):
    '''
    @jie
        找到父目录 将新目录添加进去
        input:
            root: 目录树根节点
            name: 文件路径
            myfile: 待添加目录指针
    '''
    father.addDirectory(mydir)


def findFartherFile(path):
    '''
    @jie
        查找文件父目录
        input:
        name [] : 文件路径 ["d1" , "d2"] 表示 "/d1/d2" 这个路径
        output:
        None : 文件不存在
        file *DIRECTORYNODE : 找到的父节点指针
    '''
    if len(path) == 0:  # 根目录
        return root
    i = 0
    p = root
    while i < len(path):
        flag = False
        for x in p.childDirectories:
            if x.filename == path[i]:
                flag = True
                p = x
                break
        if flag:
            i += 1
        else:
            return None
    return p


def findFile(path):
    '''
    @jie
        查找文件
        input
            root: 跟目录
            name: 文件路径
        output
            FILENODE* 找到对应的文件
            None  未找到
    '''
    filename = path[-1]
    fatherDir = findFartherFile(path[:-1])
    if fatherDir is not None:
        for x in fatherDir.childFiles:
            if x.filename == filename:
                return x
        return None  # 没找到
    else:
        return None


def listFiles(path):
    result = []
    Dir = findFartherFile(path)
    if Dir is not None:
        for x in Dir.childDirectories:
            result.append(x.filename)
        for x in Dir.childFiles:
            result.append(x.filename)
    return result


def addFileToDirectory(name, myfile):
    '''
    @jie
        找到父目录 将新文件添加进去
        input:
            root: 目录树根节点
            name: 文件路径
            myfile: 待添加文件指针
    '''
    father = findFartherFile(root, name)
    if father is None:
        return False
    else:
        father.addFile(myfile)
        return True


def pathParse(path):
    '''
    @jie
    文件路径解析
    input
      path string "/test/test"
    output
      ["test","test"]
    '''
    path = path.split('/')
    res = []
    for x in path:
        if x != '':
            res.append(x)
    return res


def isDirExit(path):
    '''
    @jie
    isDirExit 判断指定路径是否存在
    input
        path ["test" , "file"]
    output
        Ture / False
    '''
    i = 0
    point = root
    while i < len(path):
        flag = False
        for x in point.childDirectories:
            if x.filename == path[i]:
                flag = True
                point = x
                break
        if flag:
            i += 1
        else:
            return False
    return True

def isFileExit(path):
    '''
    @jie
    :param path: 文件路径数组 ["test" , "x.txt"] 表示/test/x.txt
    :return:
        文件是否存在
    '''
    filename = path[-1]
    path = path[:-1]
    father = findFartherFile(path)
    if father is None:
        return False
    for x in father.childFiles:
        if x.filename == filename:
            return True
    return False


def action():
    while True:
        ftp = FTP()
        for x in range(len(FC.ips)):
            try:
                ftp.connect(FC.ips[x], 21)
                ftp.login("ftpuser", "ftppass")
                print(ftp.pwd())
                ftp.close()
                FC.flag[x] = True
                print(FC.ips[x] + " OK!\n")
            except:
                FC.flag[x] = False
                print(FC.ips[x] + " can not connect!\n")
        time.sleep(60)


def deletefile(dir , filename):
    for x in dir.childFiles:
        if x.filename == filename:
            break
    if (x is not None) and (x.filename == filename):
        # 父目录里清除这条记录
        dir.childFiles.remove(x)
        dir.fileNum -= 1

        # 先删除datanode存的所有的文件块
        locations = x.locations
        [name, extname] = os.path.splitext(filename)
        ftp = FTP()
        for loc in locations:
            ftp.connect(loc[0], 21)
            ftp.login("ftpuser", "ftppass")
            remotefilename = filename + loc[1] + extname
            ftp.delete(remotefilename)
            ftp.close()

        #删除块链
        head = x.head
        while head is not None:
            p = head.next
            del head
            head = p

        # 删除目录树上这个文件节点
        del x

def deleteDir(dir):
    if dir.fileNum > 0:
        for x in dir.childFiles:
            deletefile(dir, x.filename)

    if dir.directoryNum > 0:
        for x in dir.childDirectories:
            deleteDir(x)
            dir.directoryNum -= 1

    if dir.directoryNum == 0:
        del dir



class main(object):
    '''
        @jie
        新建文件夹
        input:
            filepath "/test"
        output:
            一个状态字符串
            file xxx is exist  ==> 文件已存在，创建失败
            file xxx not exist ==> 路径中有文件不存在
            ok!                ==> 创建成功
    '''
    def mkdir(self, path):
        parsedPath = pathParse(path)
        if len(parsedPath) == 0:
            return "the file " + path + " is exist!"
        filename = parsedPath[-1]
        parsedPath = parsedPath[:-1]
        if isDirExit(parsedPath):
            father = findFartherFile(parsedPath)
            for x in father.childDirectories:
                if x.filename == filename:
                    return filename + " exist!"
            myDir = FC.DIRECTORYNODE()
            myDir.filename = filename
            father.addDirectory(myDir)
            return "ok!"
        else:
            path = "/" + "/".join(parsedPath)
            return path + " not exist!"

    '''
    @jie
    获取文件分块大小
    input:
        无
    output:
        服务器端设定的文件块大小
    '''
    def getBlockSize(self):
        return 1024

    '''
        @jie
        获取文件块存储位置
        input:
            path  ==>  文件存储路径 要带文件名
            num   ==>  文件块数量
        output:
            location  ==> 各块存储位置
            [
                [[ip , idx],[ip , idx]], 第0个block的位置 主和副本 这里只设置一个副本
                [[ip , idx],[ip , idx]], 第1个block的位置
                ...
                [[ip , idx],[ip , idx]], 第num - 1个block的位置
            ]
        '''
    def getLocation(self, path, num):
        # TODO 如果用户输入的path没有到具体文件而是一个文件夹要不要做异常处理？
        parsedPath = pathParse(path)
        if isFileExit(parsedPath):
            return []
        filename = parsedPath[-1]
        parsedPath = parsedPath[:-1]
        print("filename " + filename)
        print(parsedPath)
        if isDirExit(parsedPath):
            file = FC.FILENODE()
            file.filename = filename
            file.blocks = num
            file.buildBlockList()
            father = findFartherFile(parsedPath)
            father.addFile(file)
            return file.locations
        else:
            return []

    '''
    @jie
    获取一个文件各块地址
    input:
        file string: 文件路径 "/x.txt"
    output:
        [] : 各块地址，每个块从原本+副本中随机挑选一个
    '''
    def get(self, file):
        parsedfile = pathParse(file)
        filenode = findFile(parsedfile)
        if filenode is not None:
            return filenode.blockLocations()
        else:
            return []

    def changeIP(self, file, blocknum, i):
        '''
        @jie 旧的IP地址对应的datanode失效 重新分配
        :param file:  文件路径
        :param blocknum: 第几块
        :param i:  哪个副本
        :return:
            更新的ip
        '''
        file = pathParse(file)
        filenode = findFile(file)
        return filenode.changeBlockLocation(blocknum, i)


    '''
    @jie
    list dir
    input: 
        dir string : 目录路径
    output:
        [] : 目录下所有文件名称
    '''
    def ls(self , dir):
        path = pathParse(dir)
        return listFiles(path)

    '''
    @jie
    文件位置移动
    逻辑：
        只要更改文件目录树就行了，将本节点记录加入到目的位置节点，然后从父节点删除本节点记录
    input:
        src: 源文件/目录
        des: 目的位置
    output:
        成功则 ok
        否则 错误提示
    '''
    def mv(self , src , des):
        parsed_des = pathParse(des)
        parsed_src = pathParse(src)
        if not isDirExit(parsed_des):
            return "file " + des + " not exist!"
        if src == "/":
            return "mv / is not allowed!"
        desfile = findFartherFile(parsed_des)
        if isDirExit(parsed_src):
            for x in desfile.childDirectories:
                if x.filename == parsed_src[-1]:
                    return "file name conflict!"
            # 将原目录从父目录删除 重新添加到目的目录
            srcfile = findFartherFile(parsed_src)
            srcfather = findFartherFile(parsed_src[:-1])
            # 添加
            desfile.addDirectory(srcfile)
            # 删除
            for x in srcfather.childDirectories:
                if x.filename == srcfile.filename:
                    srcfather.childDirectories.remove(x)
                    break
            srcfather.directoryNum -= 1
            return "ok!"
        elif isFileExit(parsed_src):
            for x in desfile.childFiles:
                if x.filename == parsed_src[-1]:
                    return "file name conflict!"
            # 将文件添加到目的目录下，删除原父目录中的记录
            file = findFile(parsed_src)
            father = findFartherFile(parsed_src[:-1])
            desfile.addFile(file)
            for x in father.childFiles:
                if x.filename == file.filename:
                    father.childFiles.remove(x)
                    father.fileNum -= 1
                    break
            return "ok!"
        else:
            return "file " + src + " not exist!"

    def rmr(self , path):
        parsedPath = pathParse(path)
        # 如果是一个文件
        if isFileExit(parsedPath):
            filename = parsedPath[-1]
            faPath = parsedPath[:-1]
            faDir = findFartherFile(faPath)
            deletefile(faDir, filename)
            return "ok!"
        elif isDirExit(parsedPath):
            if len(parsedPath) == 0:
                return "delete / is not allowed!"
            faDir = findFartherFile(parsedPath[:-1])
            thisdir = findFartherFile(parsedPath)
            faDir.childDirectories.remove(thisdir)
            faDir.directoryNum -= 1
            deleteDir(thisdir)
            return "ok!"
        else:
            return "file or directory not exist!"

    def rm(self , path):
        parsedPath = pathParse(path)
        # 如果是一个文件
        if isFileExit(parsedPath):
            filename = parsedPath[-1]
            faPath = parsedPath[:-1]
            faDir = findFartherFile(faPath)
            deletefile(faDir, filename)
            return "ok!"
        elif isDirExit(parsedPath):
            if len(parsedPath) == 0:
                return "delete / is not allowed!"
            faDir = findFartherFile(parsedPath[:-1])
            thisdir = findFartherFile(parsedPath)
            if thisdir.fileNum == 0 and thisdir.directoryNum == 0:
                faDir.childDirectories.remove(thisdir)
                faDir.directoryNum -= 1
                del thisdir
                return "ok!"
            else:
                return path + "is not an empty directory! use '-r' force to remove."
@atexit.register
def dump():
    # 固化文件目录树
    pk.dump(root, open("./dirTree.pkl", "wb"))


if __name__ == '__main__':
    # 启动节点活跃性检测进程
    # thread = threading.Thread(target=action, args=())
    # thread.start()
    if os.path.exists("./dirTree.pkl"):
        # 文件目录树已存在 直接加载
        print("load dir tree......")
        root = pk.load(open("./dirTree.pkl", 'rb'))
    else:
        # 文件目录树不存在 新建
        root = FC.DIRECTORYNODE()
        root.filename = "/"
    s = zerorpc.Server(main())
    s.bind("tcp://0.0.0.0:4242")
    s.run()
