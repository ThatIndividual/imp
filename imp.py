#!/usr/bin/env python3
import asm

NOOP = 0x00  # ( -- )
DROP = 0x01  # (a -- )
LOAD = 0x02  # ( -- a)
DUP  = 0x03  # (a -- aa)
SWAP = 0x04  # (ab -- ba)
OVER = 0x05  # (ab -- aba)
ROT  = 0x06  # (abc -- bca)
UROT = 0x07  # (abc -- cab)
NIP  = 0x08  # (ab -- b)
TUCK = 0x09  # (ab -- aba)

ADD = 0x0A  # (ab -- c)
INC = 0x0B  # (a -- b)
DEC = 0x0C  # (a -- b)
SUB = 0x0D  # (ab -- c)
MUL = 0x0E  # (ab -- c)
DIV = 0x0F  # (ab -- c)
MOD = 0x10  # (ab -- c)

JUMP  = 0x11  # ( -- )
EQJP  = 0x12  # (ab -- )
GTJP  = 0x13  # (ab -- )
LTJP  = 0x14  # (ab -- )
EQZJP = 0x15  # (a -- )
GTZJP = 0x16  # (a -- )
LTZJP = 0x17  # (a -- )

IN  = 0x18  # ( -- a)
OUT = 0x19  # (a -- )


class Imp(object):
    def __init__(self, debug, data, ins):
        self.debug = debug
        self.data = data
        self.ins = ins
        self.ip = 0
        self.stack = []

    def run(self):
        while True:
            if self.debug:
                print(self.stack)
            ret = self.execute()
            if ret == -1:
                break
            else:
                self.ip += ret

    def execute(self):
        if self.ip == len(self.ins):
            return -1
        else:
            ins = self.ins[self.ip]
            if self.debug:
                print(str(self.ip) + " -- " + format(ins, '02X'))

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
            elif ins == UROT:
                c = self.stack.pop()
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(c)
                self.stack.append(a)
                self.stack.append(b)
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
                res = a // b
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
                b = self.stack.pop()
                a = self.stack.pop()
                if a == b:
                    self.ip = addr
                    return 0
                else:
                    return 2
            elif ins == GTJP:
                addr = self.ins[self.ip + 1]
                b = self.stack.pop()
                a = self.stack.pop()
                if a > b:
                    self.ip = addr
                    return 0
                else:
                    return 2
            elif ins == LTJP:
                addr = self.ins[self.ip + 1]
                b = self.stack.pop()
                a = self.stack.pop()
                if a < b:
                    self.ip = addr
                    return 0
                else:
                    return 2
            elif ins == EQZJP:
                addr = self.ins[self.ip + 1]
                a = self.stack.pop()
                if a == 0:
                    self.ip = addr
                    return 0
                else:
                    return 2
            elif ins == GTZJP:
                addr = self.ins[self.ip + 1]
                a = self.stack.pop()
                if a > 0:
                    self.ip = addr
                    return 0
                else:
                    return 2
            elif ins == LTZJP:
                addr = self.ins[self.ip + 1]
                a = self.stack.pop()
                if a < 0:
                    self.ip = addr
                    return 0
                else:
                    return 2
            elif ins == IN:
                self.stack.append(int(input(" < ")))
            elif ins == OUT:
                print(" > " + str(self.stack.pop()))

            return 1


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        routine = asm.asm(sys.argv[1])
        imp = Imp(False, **routine)
        imp.run()
    else:
        print("Usage: imp routine.imp")
