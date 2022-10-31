import time

class Logger:
    def __init__(self, path):
        self.path = path

    def writeAccesslog(self, content):
        with open(self.path + '/access.log', 'a+') as f:
            f.write(time.asctime() + '        ' + content)
        f.close()

    def writeErrorlog(self, content):
        with open(self.path + '/error.log', 'a+') as f:
            f.write(time.asctime() + '        ' + content)
        f.close()


