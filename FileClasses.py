import queue

# 文件基础类 记录一些文件基础信息，如文件名
class INODE:
	# 文件名称
	filename = ""

	#构造函数
	def __init__(self):
		self.filename = ""

class BLOCKNODE:
	def __init__(self):
		# 块存储位置
		self.location = ""
		# 块的大小
		self.size = 0
		# 链接下一个块 这里是否需要后面再看
		self.next = None


# 文件节点类
class FILENODE(INODE):
	def __init__(self):
		INODE.__init__(self)
		# 当前文件有多少个块
		self.blocks = 0
		# 块链表头
		self.head = None

		# TODO: 备份怎么处理呢？
		# 先默认一个备份
		self.copyNum = 1
		# 备份块链表头，只设置一个备份则数组里就一个元素
		self.copies = []

	# 构造块链 带头结点的链表
	def buildBlockList(self):
		blockhead = BLOCKNODE()
		p = blockhead
		for i in range(self.blocks):
			block = BLOCKNODE()
			# TODO: 块大小要不要作为参数传进来
			block.size = 100
			# TODO: 存储位置如何获取？
			block.location = "location"
			p.next = block
			p = block
		self.head = blockhead

	# 构造备份块链 带头结点的链表
	def buildCopyList(self):
		for i in range(self.copyNum):
			p = blockhead = BLOCKNODE()
			for i in range(self.blocks):
				block = BLOCKNODE()
				# TODO: 块大小要不要作为参数传进来
				block.size = 100
				# TODO: 存储位置如何获取？
				block.location = "copy_location"
				p.next = block
				p = block
			self.copies.append(blockhead)

# 目录节点类
class DIRECTORYNODE(INODE):
	def __init__(self):
		INODE.__init__(self)
		# 本目录里目录数
		self.directoryNum = 0
		# 本目录里文件数
		self.fileNum = 0
		# 数组 存储子目录指针
		self.childDirectories = []
		#数组 存储子文件指针
		self.childFiles = []

	def addDirectory(self, dir):
		self.directoryNum += 1
		self.childDirectories.append(dir)

	def addFile(self, file):
		self.fileNum += 1
		self.childFiles.append(file)

# 找到父目录 将新文件添加进去
# TODO 查找的逻辑是有问题的 应该根据文件路径去找父目录 暂时只写一个简单的测试
def addFileToDirectory(root, name , myfile):
	# BFS 找
	q = queue.Queue()
	q.put(root)
	top = None
	while (not q.empty()):
		top = q.get()
		if (top.name == name):
			break
		for x in top.childDirectories:
			q.put(x)
	if top.name == name:
		top.addFile(myfile)
	else:
		print("directory is not exist")

# 找到父目录 将新目录添加进去
# TODO 查找的逻辑是有问题的 应该根据文件路径去找父目录 暂时只写一个简单的测试
def addDirectoryToDirectory(root, name , myDir):
	# BFS 找
	q = queue.Queue()
	q.put(root)
	top = None
	while (not q.empty()):
		top = q.get()
		if (top.name == name):
			break
		for x in top.childDirectories:
			q.put(x)
	if top.name == name:
		top.addDirectory(myDir)
	else:
		print("directory is not exist")

def findFartherFile(root , name):
	'''
	@jie
	查找文件父目录
	input:
		name string : 文件路径 "/d1/d2"
	output:
		None : 文件不存在
		file *DIRECTORYNODE : 找到的父节点指针
	'''
	print(name)
	if name[0] == '/':
		name = name[1:]
	if name[-1] == '/':
		name = name[:-1]
	files = name.split('/')
	i = 1
	flag = False

	

	


if __name__ == "__main__":
	'''
	# 根节点 "/"
	root = DIRECTORYNODE()
	root.name = "/"

	# 新建一个目录 "/test"
	test = DIRECTORYNODE()
	test.name = "test"
	addDirectoryToDirectory(root , "/" , test)

	# 新建1个文件 "/test/file.txt" 假设需要两个block
	file1 = FILENODE()
	file1.name = "file"
	file1.blocks = 2
	file1.buildBlockList()
	file1.buildCopyList()
	addFileToDirectory(root, "test", file1)

	#打印结果
	q = queue.Queue()
	q.put(root)
	top = None
	while (not q.empty()):
		top = q.get()
		print(top.name)
		if isinstance(top, FILENODE):
			p = top.head.next
			cnt = 0
			while p != None:
				cnt += 1
				p = p.next
			print("块数量" , cnt)
			print(top.copies[0])
		else:
			print("子目录有", top.directoryNum)
			print("子文件有", top.fileNum)
			for x in top.childDirectories:
				q.put(x)
			for x in top.childFiles:
				q.put(x)
	'''
	findFartherFile("/test/he/")
