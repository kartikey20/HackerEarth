import os
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


def solve(n, q, ls, queries):
    for x in queries:
        ls[x[0] - 1] = x[1]
    print(ls)
    k = len(ls) - len(set(ls))
    return n - k + 1


res = []
T = int(input())
for _ in range(T):
    N, Q = map(int, input().split())
    arr = list(map(int, input().split()))
    LR = []
    for _ in range(Q):
        LR.append(list(map(int, input().split())))
    res.append(solve(N, Q, arr, LR))

for x in res:
    print(x)

[5, 6, 1, 3, 1, 12, 7, 18, 6, 3]
6  4  9  7  10  2  3   1  5  8
