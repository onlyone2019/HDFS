import zerorpc

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")
# print(c.mkDir("/test"))
# print(c.mkDir("/test/xxxx"))
print(c.ls("/"))
print(c.ls("/test"))