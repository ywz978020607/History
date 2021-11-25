#include <stdio.h>
 
extern "C" {
    __declspec(dllexport) int Double(int x);
    __declspec(dllexport) float floatAdd(float a,float b); 
    __declspec(dllexport) double doubleAdd(double a,double b);
    __declspec(dllexport) double* double_selfadd1(double *a,int len); 
    __declspec(dllexport) void HelloWorld(char * str); 
    __declspec(dllexport) void Ints(int * arr,int n); 
}
 
int Double(int x){
    return x*2;
}

float floatAdd(float a,float b) {
    return a+b;
}

double doubleAdd(double a,double b){
    return a+b;
}


double* double_selfadd1(double *a,int len){
    int i;
	printf("in C:a[i] \t");
	for(i = 0; i<len; i++){  
		printf("%.3lf ", a[i]); 
		a[i]+=2.0;
	}
	printf("\n");
	return a;
}


void HelloWorld(char * str){
    puts(str);
}

void Ints(int * arr,int n){
    for(int i=0;i<n;i++){
        printf("%d ",arr[i]);
    }
    puts("");
}