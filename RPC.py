import zerorpc


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



s = zerorpc.Server(caculate())

s.bind("tcp://0.0.0.0:4242")
s.run()