#include <unistd.h>
#include <stdio.h>
extern int test();
int main()
{
    while (1){
        int x = test();
        printf("%d\n",x);
        sleep(1);
    }
}
