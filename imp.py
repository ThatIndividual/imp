#!/usr/bin/env python3

NOOP = 0x00    # ( -- )
DROP = 0x01    # (a -- )
LOAD = 0x02    # ( -- a)
DUP = 0x03  # (a -- aa)
SWAP = 0x04    # (ab -- ba)
OVER = 0x05    # (ab -- aba)
ROT = 0x06  # (abc -- bca)
NIP = 0x07     # (ab -- b)
TUCK = 0x08    # (ab -- aba)

ADD = 0x09  # (ab -- c)
INC = 0x0A
DEC = 0x0B
SUB = 0x0C
MUL = 0x0D
DIV = 0x0E
MOD = 0x0F

JUMP = 0x10
EQJP = 0x11
GTJP = 0x12
LTJP = 0x13
EQZJP = 0x14
GTZJP = 0x15
LTZJP = 0x16

class Imp(object):
    def __init__(self, data, ins):
        self.data = data
        self.ins = ins
        self.ip = 0
        self.stack = []

    def run(self):
        while True:
            ret = self.execute()
            if ret == -1:
                break
            else:
                self.ip += ret
            # print(self.stack)
        print(self.stack)

    def execute(self):
        if self.ip == len(self.ins):
            return -1
        else:
            ins = self.ins[self.ip]
            # print(str(self.ip) + " -- " + format(ins, '02X'))

            if ins == NOOP:
                pass
            elif ins == DROP:
                self.stack.pop()
            elif ins == LOAD:
                index = self.ins[self.ip + 1]
                self.stack.append(self.data[index])
                return 2
            elif ins == DUP:
                self.stack.append(self.stack[-1])
            elif ins == SWAP:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(b)
                self.stack.append(a)
            elif ins == OVER:
                self.stack.append(self.stack[-2])
            elif ins == ROT:
                c = self.stack.pop()
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(b)
                self.stack.append(c)
                self.stack.append(a)
            elif ins == NIP:
                self.stack.pop(-2)
            elif ins == TUCK:
                self.stack.append(self.stack[-2])
            elif ins == ADD:
                b = self.stack.pop()
                a = self.stack.pop()
                res = a + b
                self.stack.append(res)
            elif ins == INC:
                self.stack[-1] += 1
            elif ins == DEC:
                self.stack[-1] -= 1
            elif ins == SUB:
                b = self.stack.pop()
                a = self.stack.pop()
                res = a - b
                self.stack.append(res)
            elif ins == MUL:
                b = self.stack.pop()
                a = self.stack.pop()
                res = a * b
                self.stack.append(res)
            elif ins == DIV:
                b = self.stack.pop()
                a = self.stack.pop()
                res = a / b
                self.stack.append(res)
            elif ins == MOD:
                b = self.stack.pop()
                a = self.stack.pop()
                res = a % b
                self.stack.append(res)
            elif ins == JUMP:
                self.ip = self.ins[self.ip + 1]
                return 0
            elif ins == EQJP:
                addr = self.ins[self.ip + 1]
                if self.stack[-2] == self.stack[-1]:
                    self.ip = addr
                    return 0
                else:
                    return 2
            elif ins == GTJP:
                addr = self.ins[self.ip + 1]
                if self.stack[-2] > self.stack[-1]:
                    self.ip = addr
                    return 0
                else:
                    return 2
            elif ins == LTJP:
                addr = self.ins[self.ip + 1]
                if self.stack[-2] < self.stack[-1]:
                    self.ip = addr
                    return 0
                else:
                    return 2
            elif ins == EQZJP:
                addr = self.ins[self.ip + 1]
                if self.stack[-1] == 0:
                    self.ip = addr
                    return 0
                else:
                    return 2
            elif ins == GTZJP:
                addr = self.ins[self.ip + 1]
                if self.stack[-1] > 0:
                    self.ip = addr
                    return 0
                else:
                    return 2
            elif ins == LTZJP:
                addr = self.ins[self.ip + 1]
                if self.stack[-1] < 0:
                    self.ip = addr
                    return 0
                else:
                    return 2

            return 1

if __name__ == "__main__":
    gcd = {
        # Computes the greatest common divisor of two numbers.
        # Those numbers must be placed in slots 0 and 1.
        "data" : [2312, 320],
        "ins" : [LOAD, 0,    # 00, 01
                 LOAD, 1,    # 02, 03
                 EQZJP, 11,  # 04, 05
                 SWAP,       # 06
                 OVER,       # 07
                 MOD,        # 08
                 JUMP, 4,    # 09, 10
                 DROP,       # 11
                 ]
    }
    is_prime = {
        # If given a prime number, it will return that same number.
        # If given a non-prime number, it will return its smallest divisor.
        "data" : [135341, 2],
        "ins" : [LOAD, 0,    # 00, 01
                 LOAD, 1,    # 02, 03
                 EQJP, 16,   # 04, 05
                 OVER,       # 06
                 OVER,       # 07
                 MOD,        # 08
                 EQZJP, 15,  # 09, 10
                 DROP,       # 11
                 INC,        # 12
                 JUMP, 4,    # 13, 14
                 DROP,       # 15
                 NIP,        # 16
                 ]
    }
    imp = Imp(**is_prime)
    imp.run()