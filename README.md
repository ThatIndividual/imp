Imp VM
======

Running bytecode
----------------

A small stack-based virtual machine intended to be used as a compiler target
(eventually).

IMP has two implementations, one in python, `imp.py` that can run plaintext
files located in the `routines` folder:

```
$ ./imp.py routines/gcd.imp
```

The other implementation is in C. It runs bytecode generated with the `asm.py`
utility:

```
$ ./asm.py input.imp output.obj
$ ./imp.elf output.obj
```

The C implementation is developed on Linux, and uses a gcc-specific extension,
computed gotos. There is no _intended_ difference between the two
implementations, so don't worry if you can't compile the C version for your
system. All you're missing is execution speed.

Writing bytecode
----------------

A basic Imp routine looks like this:

```
; Routine for addind 2 and 3 together.
DAT
    2 3
INS
    load 0  ; Push 2 on the stack
    load 1  ; Push 3 on the stack
    add     ; Pop the two topmost values off the stack, add them, and push the
            ; result back on the stack.
    out     ; Pop the stack and print the popped value.
```

As you can see, it has two sectors, one for data and another for instructions,
called DAT and INS respectively.

While reading a routine, the Imp VM reads the instructions one by one (and
their arguments) and executes them. All instructions implicitly interact with
the stack. Some instructions may interact with the instruction pointer. Plainly
speaking, modifying the instruction pointer means either rerunning some
instructions or skipping them altogether. These *jumps* always take a number as
an argument, pointing them to where the instruction pointer must point next.
However, providing an absolute position is tedious and error-prone, so we
provide *tags*.

For example:

```
; Routine that prints numbers from 0 to 9.
; For the sake of brevity, pop and push refer exclusively to the stack.
DAT
    0 10
INS
        load 0      ; Push 0.
loop:           ; Tag this position as "loop".
        dup         ; Copy the top of the stack and push it.
        out         ; Pop and print that value.
        inc         ; Increment the top of the stack.
        load 1      ; Push 10.
        over        ; Copy the value after the top of the stack and push it.
        eqjp @loop  ; Pop the two topmost values and if they are equal, jump
                    ; back to "loop".
```

Complete instruction listing
----------------------------

  Name  | Stack effect | Description
--------|--------------|------------
noop    |( -- )        | Does nothing.
drop    |(a -- )       |
load x  |( -- a)       | Load value at position x in the data sector.
dup     |(a -- aa)     |
swap    |(ab -- ba)    |
over    |(ab -- aba)   |
rot     |(abc -- bca)  |
nip     |(ab -- b)     |
tuck    |(ab -- aba)   |
add     |(ab -- c)     |
inc     |(a -- b)      | Increments a value by one.
dec     |(a -- b)      | Decrements a value by one.
sub     |(ab -- c)     |
mul     |(ab -- c)     |
div     |(ab -- c)     |
mod     |(ab -- c)     |
jump x  |( -- )        | Change the instruction pointer to position x.
eqjp x  |(ab -- )      | If a == b jump to x.
gtjp x  |(ab -- )      | If a > b  jump to x.
ltjp x  |(ab -- )      | If a < b  jump to x.
eqzjp x |(a -- )       | If a == 0 jump to x.
gtzjp x |(a -- )       | If a > 0  jump to x.
ltzjp x |(a -- )       | Unusable.
in      |( -- a)       | Get user input and push it.
out     |(a -- )       | Pop value and print it.

