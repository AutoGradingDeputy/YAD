int functionA(int a, int b){
    return a + b;
}

int functionB(int a, int b){
    return a + b;
}

float functionB(int a, float b){
    return (float)a + b;
}

int functionC(int a, int b){
    if(a+b > 20)
        return a+b;
    functionC(a+1, b+1);
}

template <typename T> int functionD(T t){
    return t;
}

int * functionE(int a, int b){
    int c;
    c = a + b;
}

int ** functionF(int a, int b){
    int c;
    c = a + b;
}

int functionJ(int &a){
    return a;
}

int functionK(int *a){
    return *a;
}
int functionL(int a[], int size){
    int sum=0;
    for(int i=0 ; i<size; i++)
        sum+=a[i];
    return sum;
}

unsigned long functionM(unsigned long a, unsigned long b){
    return a+b;
}

double functionN(const int k, double w){
    return w;
}

int main (){
    cout <<" HELLO ";
}