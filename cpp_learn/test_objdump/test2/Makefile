
all:
	objcopy -I binary -O elf64-x86-64 -B i386:x86-64 foo.c foo-src.o
	gcc -g -fPIC -c -o foo2.o foo2.c
	gcc -g -fPIC -c -o foo.o foo.c
	gcc -g -fPIC -shared -o libfoo-src.so foo-src.o
	gcc -g -fPIC -shared -o libfoo2.so foo2.c -L. -lfoo-src
	gcc -g -o foo.exe foo.o -L. -lfoo2

clean:
	rm -f *~
	rm -f *.so *.exe *.o
