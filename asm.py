import re

str_ops = {
    "noop": 0x00,
    "drop": 0x01,
    "load": 0x02,
    "dup" : 0x03,
    "swap": 0x04,
    "over": 0x05,
    "rot" : 0x06,
    "nip" : 0x07,
    "tuck": 0x08,

    "add": 0x09,
    "inc": 0x0A,
    "dec": 0x0B,
    "sub": 0x0C,
    "mul": 0x0D,
    "div": 0x0E,
    "mod": 0x0F,

    "jump": 0x10,
    "eqjp": 0x11,
    "gtjp": 0x12,
    "ltjp": 0x13,
    "eqzjp": 0x14,
    "gtzjp": 0x15,
    "ltzjp": 0x16,
}


def cleanup(text):
    text = re.sub(r';.*', '', text)
    ops = re.split(r'[ \n]+', text)
    ops = filter(lambda x: x, ops)
    return list(ops)


def asm(filename):
    with open(filename, "r") as file:
        text = file.read()
    ops = cleanup(text)

    routine = { "data": None, "ins": None }
    if "DATA" not in ops:
        raise Exception("All programs must begin with a data sector. " + \
                        "Even if empty.")
    if "INS" not in ops:
        raise Exception("Instruction sector is missing.")
    else:
        ins_start = ops.index("INS")
    routine["data"] = list(map(int, ops[1:ins_start]))

    labels = {}
    refs = []
    ip = 0
    ops = ops[ins_start+1:]
    while ip != len(ops):
        op = ops[ip]
        # check if label and remember position
        if op[-1] == ":":
            labels[(op[:-1])] = ip
            ops.pop(ip - len(ops))
            ip += 0
        # check if reference, and mark in refs
        elif op[0] == "@":
            ops[ip] = op[1:]
            refs.append(ip)
            ip += 1
        # check if opcode and turn to code
        elif op in str_ops:
            ops[ip] = str_ops[op]
            ip += 1
        # else, it's an int
        else:
            ops[ip] = int(op)
            ip += 1
    # turn references to actual locations
    for ref in refs:
        ops[ref] = labels[ops[ref]]
    routine["ins"] = ops
    return routine
