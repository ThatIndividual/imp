#include <stdio.h>
#include <stdlib.h>
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
    OUT = 0x18
};

char *to_str[] = {
    "noop", "drop", "load", "dup", "swap", "over", "rot", "nip", "tuck", "add",
    "inc", "dec", "sub", "mul", "div", "mod", "jump", "eqjp", "gtjp", "ltjp",
    "eqzjp", "gtzjp", "ltzjp", "in", "out"
};

void read_obj(const char *filename);
int  op_has_arg(enum op op);

int main(int argc, const char *argv[])
{
    if (argc == 2)
        read_obj(argv[1]);
    else
        printf("Usage: imp routine.obj\n");
}

void read_obj(const char *filename)
{
    FILE *file = fopen(filename, "rb");

    /* read version; 2 bytes */
    uint8_t maj_ver, min_ver;
    fread(&maj_ver, 1, 1, file);
    fread(&min_ver, 1, 1, file);
    printf("Obj ver %"PRIu8".%"PRIu8"\n", maj_ver, min_ver);

    /* read no of datapoints; 1 byte */
    uint8_t no_data;
    fread(&no_data, 1, 1, file);

    /* read datapoints; 4 bytes */
    uint32_t *data;
    data = calloc(no_data, 4);
    fread(data, 4, no_data, file);

    puts("DAT");
    for (int i = 0; i < no_data; ++i) {
        printf("%3i    %"PRIu32"\n", i, data[i]);
    }

    /* read no of instructions; 1 byte */
    uint8_t no_ins;
    fread(&no_ins, 1, 1, file);

    /* read instructions; 1 byte */
    uint8_t *ins;
    ins = calloc(no_ins, 1);
    fread(ins, 1, no_ins, file);

    puts("INS");
    for (int i = 0; i < no_ins;) {
        uint8_t op = ins[i];
        if (op_has_arg(op)) {
            printf("%3i    %s %"PRIu8"\n", i, to_str[op], ins[i+1]);
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

