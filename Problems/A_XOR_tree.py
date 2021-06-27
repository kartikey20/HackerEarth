from itertools import combinations
import os
from functools import reduce
import sys
from io import BytesIO, IOBase
BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.write = self.buffer.write if self.writable else None

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b'\n') + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.write = lambda s: self.buffer.write(s.encode('ascii'))
        self.readline = lambda: self.buffer.readline().decode('ascii')


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
def input(): return sys.stdin.readline().rstrip('\r\n')


def solve(n, edges, nodes):
    sum = 0
    dic = {x: [] for x in nodes}
    for x in edges:
        dic[nodes[x[0] - 1]].append(nodes[x[1] - 1])
    for key, value in dic.items():
        for x in value:
            sum += reduce(lambda i, j: i ^ j, [key, x])
        if len(value) > 1:
            sum += reduce(lambda i, j: i ^ j, value + [key])
    return sum


T = int(input())
res = []
for _ in range(T):
    N = int(input())
    edges = [0] * (N - 1)
    nodes = list(map(int, input().split()))
    for i in range(N - 1):
        edges[i] = list(map(int, input().split()))
    res.append(solve(N, edges, nodes))

for x in res:
    print(x)
