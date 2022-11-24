import queue
from this import d

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
	if name[0] == '/':
		name = name[1:]
	if len(name) == 0: # 根目录
		return root
	if name[-1] == '/':
		name = name[:-1]
	files = name.split('/')
	i = 0
	while(i < len(files)):
		flag = False
		for x in root.childDirectories:
			if x.name == files[i]:
				i = i + 1
				flag = True
				root = x
				break
		if flag :
			i += 1
		else:
			return None
	return root

def findFile(root ,name):
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
	if len(name) == 0 or name[-1] == '/': # 不应该有 "/" "/test/"这样的文件路径
		return None
	files = name.split('/')
	filename = files[-1]
	name = name[:-len(filename)]
	fatherDir = findFartherFile(root , name)
	if fatherDir != None:
		for x in fatherDir.childFiles:
			if x.name == filename:
				return x
		return None  # 没找到
	else:
		return None

def listFiles(root , name):
	result = []
	Dir = findFartherFile(root , name)
	if Dir != None:
		for x in Dir.childDirectories:
			result.append(x.name)
		for x in Dir.childFiles:
			result.append(x.name)
	return result

def addFileToDirectory(root, name , myfile):
	'''
	@jie
		找到父目录 将新文件添加进去
		input:
			root: 目录树根节点
			name: 文件路径
			myfile: 待添加文件指针
	'''
	father = findFartherFile(root , name)
	if father == None:
		return False
	else:
		father.addFile(myfile)
		return True

def addDirectoryToDirectory(root, name , myDir):
	'''
	@jie
		找到父目录 将新目录添加进去
		input:
			root: 目录树根节点
			name: 文件路径
			myfile: 待添加目录指针
	'''
	father = findFartherFile(root , name)
	if father == None:
		return False
	else:
		father.addDirectory(myDir)
		return True

if __name__ == "__main__":
	# 根节点 "/"
	root = DIRECTORYNODE()
	root.name = "/"

	# 新建一个目录 "/test"
	test = DIRECTORYNODE()
	test.name = "test"
	if addDirectoryToDirectory(root , "/" , test) == False:
		print("add directory error!")

	# 新建1个文件 "/test/file.txt" 假设需要两个block
	file1 = FILENODE()
	file1.name = "file"
	file1.blocks = 2
	file1.buildBlockList()
	file1.buildCopyList()
	if addFileToDirectory(root, "/test/", file1) == False:
		print("add file error!")

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
			# print(top.copies[0])
		else:
			print("子目录有", top.directoryNum)
			print("子文件有", top.fileNum)
			for x in top.childDirectories:
				q.put(x)
			for x in top.childFiles:
				q.put(x)



'''
需要进一步讨论的点：
	每个块具体存储位置怎么处理？
	如果文件没有处理 释放空间这部分代码写不写？
	是否设计 ls 功能 (先加上好了)
'''
