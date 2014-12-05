
rm -f *.o
gcc so1/test.cpp -shared -fPIC -o so1/libtest.so
gcc so2/test.cpp -shared -fPIC -o so2/libtest.so
