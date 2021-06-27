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


def solve(ls):
    rowLen = len(ls[0])
    colLen = len(ls)
    count = 0
    for row in range(rowLen):
        for col in range(colLen):
            x = ls[row][col]
            for row2 in range(row, rowLen):
                for col2 in range(col, colLen):
                    y = ls[row2][col2]
                    if x > y:
                        count += 1
    return count


T = int(input())
res = []
for _ in range(T):
    N = int(input())
    arr = []
    for row in range(N):
        arr.append(list(map(int, input().split())))
    res.append(solve(arr))

for x in res:
    print(x)
