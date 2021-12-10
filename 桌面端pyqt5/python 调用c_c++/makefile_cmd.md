#linux,windows:  .so
gcc helloWorld.c -fPIC -shared -o libhello.so
g++ dlltest2.cpp -fPIC -shared -o dlltest2.so

#windows:       .dll
gcc dlltest.c -shared -o dlltest.dll -Wl,--out-implib,dlltest.lib
g++ dlltest2.cpp -shared -o dlltest2.dll -Wl,--out-implib,dlltest2.lib