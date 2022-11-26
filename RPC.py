import zerorpc
import queue
import random
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

root = FC.DIRECTORYNODE()
root.name = "/"

def addDirectoryToDirectory(father, myDir):
    '''
    @jie
        找到父目录 将新目录添加进去
        input:
            root: 目录树根节点
            name: 文件路径
            myfile: 待添加目录指针
    '''
    father.addDirectory(myDir)

def findFartherFile(path):
    '''
    @jie
        查找文件父目录
        input:
        name string : 文件路径 "/d1/d2"
        output:
        None : 文件不存在
        file *DIRECTORYNODE : 找到的父节点指针
    '''
    if len(path) == 0:  # 根目录
        return root
    i = 0
    p = root
    while (i < len(path)):
        flag = False
        for x in p.childDirectories:
            if x.name == path[i]:
                flag = True
                p = x
                break
        if flag:
            i += 1
        else:
            return None
    return p

def findFile(name):
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
    if name[0] == '/':
        name = name[1:]
    if len(name) == 0 or name[-1] == '/':  # 不应该有 "/" "/test/"这样的文件路径
        return None
    files = name.split('/')
    filename = files[-1]
    name = name[:-len(filename)]
    fatherDir = findFartherFile(name)
    if fatherDir != None:
        for x in fatherDir.childFiles:
            if x.name == filename:
                return x
        return None  # 没找到
    else:
        return None

def listFiles(name):
    result = []
    Dir = findFartherFile(root, name)
    if Dir != None:
        for x in Dir.childDirectories:
            result.append(x.name)
        for x in Dir.childFiles:
            result.append(x.name)
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
    if father == None:
        return False
    else:
        father.addFile(myfile)
        return True

def pathParse(path):
    # @jie
    # 文件路径解析
    # input
    #   path string "/test/test"
    # output
    #   ["test","test"]
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
    while (i < len(path)):
        flag = False
        for x in point.childDirectories:
            if x.name == path[i]:
                flag = True
                point = x
                break
        if flag:
            i += 1
        else:
            return False
    return True

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
    def mkDir(self , path):
        parsedPath = pathParse(path)
        if len(parsedPath) == 0:
            return "the file " + path + " is exist!"
        filename = parsedPath[-1]
        parsedPath = parsedPath[:-1]
        if isDirExit(parsedPath):
            father = findFartherFile(parsedPath)
            for x in father.childDirectories:
                if x.name == filename:
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
    def getLocation(self , path , num):
        # TODO 如果用户输入的path没有到具体文件而是一个文件夹要不要做异常处理？
        parsedPath = pathParse(path)
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








s = zerorpc.Server(main())
s.bind("tcp://0.0.0.0:4242")
s.run()