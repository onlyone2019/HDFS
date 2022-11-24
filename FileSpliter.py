import os
from filesplit.split import Split
split = Split("./x.txt", "./output")
split.bysize(size = 1024) # 每个文件最多 10MB
filename = "x.txt"  # 需要进行分割的文件，请修改文件名


from filesplit.merge import Merge
merge = Merge(inputdir = "./output", outputdir="./merge", outputfilename = "merge.txt")
merge.merge()

# size = 1000  # 分割大小约80K


# def mk_SubFile(srcName, sub, buf):
#     [des_filename, extname] = os.path.splitext(srcName)
#     filename = des_filename + '_' + str(sub) + extname
#     print('正在生成子文件: %s' % filename)
#     with open(filename, 'wb') as fout:
#         fout.write(buf)
#         return sub + 1
#
#
# def split_By_size(filename, size):
#     with open(filename, 'rb') as fin:
#         buf = fin.read(size)
#         sub = 1
#         while len(buf) > 0:
#             sub = mk_SubFile(filename, sub, buf)
#             buf = fin.read(size)
#     print("ok")
#
#
# if __name__ == "__main__":
#     split_By_size(filename, size)