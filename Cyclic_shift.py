import os
import sys
from io import BytesIO, IOBase

_str = str
str = lambda x=b'': x if type(x) is bytes else _str(x).encode()

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = 'x' in file.mode or 'r' not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

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
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode('ascii'))
        self.read = lambda: self.buffer.read().decode('ascii')
        self.readline = lambda: self.buffer.readline().decode('ascii')


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
def input(): return sys.stdin.readline().rstrip('\r\n')


def solve(_, k, s):
    temp = s[:]
    maxInt = int(s, 2)
    shift = 0
    found = 0
    while True:
        temp = temp[1:] + temp[0]
        maxInt = max(maxInt, int(temp, 2))
        if temp == s:
            break
    print(maxInt)
    binStr = "{0:b}".format(maxInt)
    temp = s[:]
    while True:
        if found == k:
            break
        else:
            shift += 1
            temp = temp[1:] + temp[0]
            if temp == binStr:
                found += 1
    return shift


T = int(input())
res = []
for _ in range(T):
    N, K = map(int, input().split())
    A = input()
    res.append(solve(N, K, A))

for x in res:
    print(x)
