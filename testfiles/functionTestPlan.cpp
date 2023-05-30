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

class test{
    int functionG(int a, int b) const{
        return a+b;
    }
    virtual void functionH() = 0;
    static int functionI(int a, int b){

    }
};

int functionJ(int &a){
    return a;
}

int functionK(int *a){
    return *a;
}