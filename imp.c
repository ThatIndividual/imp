#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>

enum op {
    NOOP = 0x00,
    DROP = 0x01,
    LOAD = 0x02,
    DUP  = 0x03,
    SWAP = 0x04,
    OVER = 0x05,
    ROT  = 0x06,
    NIP  = 0x07,
    TUCK = 0x08,

    ADD = 0x09,
    INC = 0x0A,
    DEC = 0x0B,
    SUB = 0x0C,
    MUL = 0x0D,
    DIV = 0x0E,
    MOD = 0x0F,

    JUMP = 0x10,
    EQJP = 0x11,
    GTJP = 0x12,
    LTJP = 0x13,
    EQZJP = 0x14,
    GTZJP = 0x15,
    LTZJP = 0x16,

    IN  = 0x17,
    OUT = 0x18,
};

struct obj {
    uint32_t *data;
     uint8_t *ins;
    struct {
        uint8_t magic_number[3];
        uint8_t maj_ver;
        uint8_t min_ver;
        uint8_t data_size;
        uint8_t ins_size;
    } header;
};

struct stack {
    uint32_t *data;
    uint32_t  index;
    uint32_t  size;
};

struct VM {
        uint32_t *data;
         uint8_t *ins;
    struct stack *stack;
         uint8_t  ip;
         uint8_t  data_size;
         uint8_t  ins_size;
};

char *to_str[] = {
    "noop", "drop", "load", "dup", "swap", "over", "rot", "nip", "tuck", "add",
    "inc", "dec", "sub", "mul", "div", "mod", "jump", "eqjp", "gtjp", "ltjp",
    "eqzjp", "gtzjp", "ltzjp", "in", "out"
};

struct obj *Obj_read(const char *filename);
      void  Obj_dump(struct obj *obj);

struct VM *VM_new (struct obj *obj);
     void  VM_run (struct VM *vm);
     void  VM_exec(struct VM *vm);

struct stack *Stack_new (void);
        void  Stack_push(struct stack *stack, uint32_t item);
    uint32_t  Stack_peek(struct stack *stack, uint32_t depth);
    uint32_t  Stack_pop (struct stack *stack);

int op_has_arg(enum op op);

int main(int argc, const char *argv[])
{
    if (argc == 2) {
        struct obj *obj = Obj_read(argv[1]);

        struct VM *vm = VM_new(obj);
        VM_run(vm);
    }
    else
        printf("Usage: imp [input.obj]\n");
}

struct obj *Obj_read(const char *filename)
{
    FILE *file = fopen(filename, "rb");

    /*
     * read header: magic number    , 3 bytes
     *              version number  , 2 bytes
     *              data size       , 1 byte
     *              instruction size, 1 byte
     */
    struct obj *obj = malloc(sizeof(struct obj));
    fread(&obj->header, 1, 7, file);

    /* read datapoints; 4 bytes */
    obj->data = calloc(obj->header.data_size, 4);
    fread(obj->data, 4, obj->header.data_size, file);

    /* read instructions; 1 byte */
    obj->ins = calloc(obj->header.ins_size, 1);
    fread(obj->ins, 1, obj->header.ins_size, file);

    return obj;
}

void Obj_dump(struct obj *obj)
{
    printf("IMP bytecode object. Protocol version: %"PRIu8".%"PRIu8"\n",
           obj->header.maj_ver, obj->header.min_ver);
    puts("DAT");
    for (int i = 0; i < obj->header.data_size; ++i) {
        printf("%3i    %"PRIu32"\n", i, obj->data[i]);
    }

    puts("INS");
    for (int i = 0; i < obj->header.ins_size;) {
        uint8_t op = obj->ins[i];
        if (op_has_arg(op)) {
            printf("%3i    %s %"PRIu8"\n", i, to_str[op], obj->ins[i+1]);
            i += 2;
        }
        else {
            printf("%3i    %s\n", i, to_str[op]);
            i += 1;
        }
    }
}

int op_has_arg(enum op op)
{
    switch (op) {
        case LOAD:
        case JUMP:
        case EQJP:
        case GTJP:
        case LTJP:
        case EQZJP:
        case GTZJP:
        case LTZJP:
            return 1;
        default:
            return 0;
    }
}

struct VM *VM_new(struct obj *obj)
{
    struct VM *vm = malloc(sizeof(struct VM));
    vm->data = obj->data;
    vm->ins = obj->ins;
    vm->stack = Stack_new();
    vm->ip = 0;
    vm->data_size = obj->header.data_size;
    vm->ins_size = obj->header.ins_size;

    return vm;
}

void VM_run(struct VM *vm)
{
    while (vm->ip != vm->ins_size) {
        VM_exec(vm);
    }
}

void VM_exec(struct VM *vm)
{
    uint32_t a, b, c;
    uint8_t addr, op;

    op = vm->ins[vm->ip];
    switch (op)
    {
        case NOOP:
            ++vm->ip;
            break;
        case DROP:
            Stack_pop(vm->stack);
            ++vm->ip;
            break;
        case LOAD:
            ++vm->ip;
            addr = vm->ins[vm->ip];
            Stack_push(vm->stack, vm->data[addr]);
            ++vm->ip;
            break;
        case DUP:
            a = Stack_peek(vm->stack, 0);
            Stack_push(vm->stack, a);
            ++vm->ip;
            break;
        case SWAP:
            b = Stack_pop(vm->stack);
            a = Stack_pop(vm->stack);
            Stack_push(vm->stack, b);
            Stack_push(vm->stack, a);
            ++vm->ip;
            break;
        case OVER:
            a = Stack_peek(vm->stack, 1);
            Stack_push(vm->stack, a);
            ++vm->ip;
            break;
        case ROT:
            c = Stack_pop(vm->stack);
            b = Stack_pop(vm->stack);
            a = Stack_pop(vm->stack);
            Stack_push(vm->stack, b);
            Stack_push(vm->stack, c);
            Stack_push(vm->stack, a);
            ++vm->ip;
            break;
        case NIP:
            b = Stack_pop(vm->stack);
            a = Stack_pop(vm->stack);
            Stack_push(vm->stack, b);
            ++vm->ip;
            break;
        case TUCK:
            b = Stack_pop(vm->stack);
            a = Stack_pop(vm->stack);
            Stack_push(vm->stack, b);
            Stack_push(vm->stack, a);
            Stack_push(vm->stack, b);
            ++vm->ip;
            break;
        case ADD:
            b = Stack_pop(vm->stack);
            a = Stack_pop(vm->stack);
            Stack_push(vm->stack, a + b);
            ++vm->ip;
            break;
        case INC:
            a = Stack_pop(vm->stack);
            Stack_push(vm->stack, a + 1);
            ++vm->ip;
            break;
        case DEC:
            a = Stack_pop(vm->stack);
            Stack_push(vm->stack, a - 1);
            ++vm->ip;
            break;
        case SUB:
            b = Stack_pop(vm->stack);
            a = Stack_pop(vm->stack);
            Stack_push(vm->stack, a - b);
            ++vm->ip;
            break;
        case MUL:
            b = Stack_pop(vm->stack);
            a = Stack_pop(vm->stack);
            Stack_push(vm->stack, a * b);
            ++vm->ip;
            break;
        case DIV:
            b = Stack_pop(vm->stack);
            a = Stack_pop(vm->stack);
            Stack_push(vm->stack, a / b);
            ++vm->ip;
            break;
        case MOD:
            b = Stack_pop(vm->stack);
            a = Stack_pop(vm->stack);
            Stack_push(vm->stack, a % b);
            ++vm->ip;
            break;
        case JUMP:
            ++vm->ip;
            addr = vm->ins[vm->ip];
            vm->ip = addr;
            break;
        case EQJP:
            ++vm->ip;
            b = Stack_pop(vm->stack);
            a = Stack_pop(vm->stack);
            if (a == b)
                vm->ip = vm->ins[vm->ip];
            else
                ++vm->ip;
            break;
        case GTJP:
            ++vm->ip;
            b = Stack_pop(vm->stack);
            a = Stack_pop(vm->stack);
            if (a > b)
                vm->ip = vm->ins[vm->ip];
            else
                ++vm->ip;
            break;
        case LTJP:
            ++vm->ip;
            b = Stack_pop(vm->stack);
            a = Stack_pop(vm->stack);
            if (a < b)
                vm->ip = vm->ins[vm->ip];
            else
                ++vm->ip;
            break;
        case EQZJP:
            ++vm->ip;
            a = Stack_pop(vm->stack);
            if (a == 0)
                vm->ip = vm->ins[vm->ip];
            else
                ++vm->ip;
            break;
        case GTZJP:
            ++vm->ip;
            a = Stack_pop(vm->stack);
            if (a > 0)
                vm->ip = vm->ins[vm->ip];
            else
                ++vm->ip;
            break;
        case LTZJP:
            ++vm->ip;
            a = Stack_pop(vm->stack);
            if (a < 0)
                vm->ip = vm->ins[vm->ip];
            else
                ++vm->ip;
            break;
        case IN:
            printf(" < ");
            scanf("%"SCNu32"", &a);
            Stack_push(vm->stack, a);
            ++vm->ip;
            break;
        case OUT:
            a = Stack_pop(vm->stack);
            printf(" > %"PRIu32"\n", a);
            ++vm->ip;
            break;
    }
}

struct stack *Stack_new(void)
{
    struct stack *stack = malloc(sizeof(struct stack));
    stack->data = calloc(2, 4);
    stack->size = 2;
    stack->index = 0;

    return stack;
}

void Stack_push(struct stack *stack, uint32_t item)
{
    stack->data[stack->index] = item;
    ++stack->index;
    if (stack->index == stack->size) {
        stack->size *= 2;
        stack->data = realloc(stack->data, stack->size * 4);
    }
}

uint32_t Stack_peek(struct stack *stack, uint32_t depth)
{
    return stack->data[stack->index - (depth + 1)];
}

uint32_t Stack_pop(struct stack *stack)
{
    --stack->index;
    return stack->data[stack->index];
}

