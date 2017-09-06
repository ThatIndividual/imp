#!/usr/bin/env python3
NOP = 0x0  # ( -- )
POP = 0x1  # (a -- )
PSH = 0x2  # ( -- a)
DUP = 0x3  # (a -- aa)
SWP = 0x4  # (ab -- ba)
OVR = 0x5  # (ab -- aba)
ROT = 0x6  # (abc -- bca)
NIP = 0x7  # (ab -- b)
TCK = 0x8  # (ab -- aba)

ADD = 0x9  # (ab -- c)
SUB = 0xA
MUL = 0xB
DIV = 0xC
MOD = 0xD


class Imp(object):
    def __init__(self, instructions):
        self.ins = instructions
        self.ip = 0
        self.stack = []

    def run(self):
        while True:
            ret = self.execute()
            if ret == -1:
                break
        print(self.stack)

    def execute(self):
        if self.ip == len(self.ins):
            return -1
        else:
            ins = self.ins[self.ip]

            if ins == NOP:
                self.ip += 1
            elif ins == POP:
                self.stack.pop()
                self.ip += 1
            elif ins == PSH:
                self.stack.append(self.ins[self.ip + 1])
                self.ip += 2
            elif ins == DUP:
                self.stack.append(self.stack[-1])
                self.ip += 1
            elif ins == SWP:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(b)
                self.stack.append(a)
                self.ip += 1
            elif ins == OVR:
                self.stack.append(self.stack[-2])
                self.ip += 1
            elif ins == ROT:
                c = self.stack.pop()
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(b)
                self.stack.append(c)
                self.stack.append(a)
                self.ip += 1
            elif ins == NIP:
                self.stack.pop(-2)
                self.ip += 1
            elif ins == TCK:
                self.stack.append(self.stack[-2])
            elif ins == ADD:
                b = self.stack.pop()
                a = self.stack.pop()
                res = a + b
                self.stack.append(res)
                self.ip += 1
            elif ins == SUB:
                b = self.stack.pop()
                a = self.stack.pop()
                res = a - b
                self.stack.append(res)
                self.ip += 1
            elif ins == MUL:
                b = self.stack.pop()
                a = self.stack.pop()
                res = a * b
                self.stack.append(res)
                self.ip += 1
            elif ins == DIV:
                b = self.stack.pop()
                a = self.stack.pop()
                res = a / b
                self.stack.append(res)
                self.ip += 1
            elif ins == MOD:
                b = self.stack.pop()
                a = self.stack.pop()
                res = a % b
                self.stack.append(res)
                self.ip += 1

if __name__ == "__main__":
    ins = [PSH, 1, PSH, 1, DUP, ROT, ADD, DUP, ROT, ADD, DUP, ROT, ADD, DUP, ROT, ADD, DUP, ROT, ADD, NIP]
    imp = Imp(ins)
    imp.run()
