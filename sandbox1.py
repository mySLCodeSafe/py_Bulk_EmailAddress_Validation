import queue

class child(queue.Queue):
    def _init(self, maxsize=0):
        self.queue = set()
    def _put(self, item):
        self.queue.add(item)
    def _get(self):
        return self.queue.pop()

test = child()
test._put ("hello")
test._put ("hello")
test._put ("hello")
test._put ("hello")
test._put ("hello")
test._put ("hello")
test._put ("shami")
test._put ("shami")
test._put ("shamilakhani")
test.join()


print ("size", test.qsize())

while not test.empty():
    print (test._get())

print ("size", test.qsize())

