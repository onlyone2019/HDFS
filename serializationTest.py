import FileClasses as FC
import _pickle as pk

def dump(root):
    queue = []
    ans = []
    queue.append(root)
    # pk.dump(front, open("./serialization/ans.pkl", "ab"))
    while len(queue) > 0:
        front = queue[0]
        ans.append(front)
        queue = queue[1:]
        if isinstance(front , FC.DIRECTORYNODE):
            # 是一个目录
            if len(front.childDirectories) > 0:
                for x in front.childDirectories:
                    queue.append(x)
            if len(front.childFiles) > 0:
                for x in front.childFiles:
                    queue.append(x)
                    head = x.head
                    while head is not None:
                        queue.append(head)
                        head = head.next
    pk.dump(ans, open("./serialization/ans.pkl", "wb"))

def load(path):
    classes = pk.load(open(path , 'rb'))
    root = classes

    queue = []
    # for x in root.hildDirectories:
    #     queue.append(x)
    for x in root.childFiles:
        head = x.head
        while head is not None:
            queue.append(head)
            head = head.next

    print(queue)




if __name__ == '__main__':
    root = FC.DIRECTORYNODE()
    root.filename = "/"

    dir1 = FC.DIRECTORYNODE()
    dir1.filename = "test"

    root.addDirectory(dir1)

    file = FC.FILENODE()
    file.filename = "x.txt"
    file.blocks = 2
    file.buildBlockList()

    root.addFile(file)
    # dump(root)
    pk.dump(root, open("./serialization/ans.pkl", "wb"))
    read = load("./serialization/ans.pkl")
    ##pk.dump(obj, open("./ans.pkl", "ab"))




