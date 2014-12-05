#include <stdio.h>
#include <stddef.h>

extern char _binary_foo_c_start;
extern char _binary_foo_c_end;
extern char _binary_foo_c_end;

char *bin_start = &_binary_foo_c_start;
char *bin_end = &_binary_foo_c_end;
//ssize_t bin_size = (ssize_t) &_binary_foo_c_size;

int print ()
{
    fprintf(stderr, "print\n");
    fprintf(stderr,"%x => %x\n", &_binary_foo_c_start, &_binary_foo_c_end);
    fprintf(stderr, "%x => %x\n", bin_start, bin_end);

    char* t1 = &_binary_foo_c_start;
    char* t2 = &_binary_foo_c_end;
    fprintf(stderr, "%x => %x\n", t1, t2);
    return 0;
}
