
all:
	objcopy -I binary -O elf64-x86-64 -B i386:x86-64 dicmap.bin dicmap.o
	gcc -g -fPIC -shared -o libdicmap.so dicmap.o
	gcc -g -fPIC -c -o foo2.o foo2.c
	gcc -g -fPIC -c -o foo1.o foo1.c
	gcc -g -fPIC -shared -o libfoo1.so foo1.o -L. -ldicmap
	gcc -g -fPIC -shared -o libfoo2.so foo2.c -L. -lfoo1
	gcc -g -o foo.exe foo.c -L. -lfoo2
clean:
	rm -f *~
	rm -f *.so *.exe *.o

###gcc -g -o foo.exe foo.c -L. -lfoo2 -fPIC
