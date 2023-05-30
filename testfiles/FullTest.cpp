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

class Aclass{
    private:
    int i;
    int j;
    int Atest(){
        return 0;
    }
};

class Bclass;

class Bclass{
    private:
    int i;
    int j;
    int Btest(){
        return 0;
    }
};

class C1class: Aclass{
    private:
    int i;
    int j;
    int C1test(){
        return 0;
    }
};

class C2class: Aclass, public Bclass{
    private:
    int i;
    int j;
    int C2test(){
        return 0;
    }
};

class C3class: C1class{
    private:
    int i;
    int j;
    int C3test(){
        return 0;
    }
};

class D1class{
    private:
    int i;
    int j;
    int D1test(){
        return 0;
    }
};

class D2class{
    friend class D1class;
    private:
    int i;
    int j;
    int D2test(){
        return 0;
    }
};

class Eclass{
    private:
    int i;
    int j;
    int Etest(int a, int b);
};

int Eclass::Etest(int a, int b){
    return 0;
}

class Fclass{
    private:
    int i;
    int j;
    
    Fclass();
    Fclass(Fclass &a);
    ~Fclass();
};

Fclass::Fclass(){
    i = 0;
    j = 1;
}

Fclass::Fclass(Fclass &a){
    this->i = a.i;
    this->j = a.j;
}

Fclass::~Fclass(){
    //GoodBye
    i = 0;
    j = 0;
}

class Gclass{
    private:
    int i;
    int j;
    
    Gclass(int a, int b);
};

Gclass::Gclass(int a, int b) : i(a), j(b){
    int x;
}

class Hclass{
    int i;
    int j;
    class H1class{
        int i;
        int j;
    };
};

class I1class {
public:
    virtual double getI() = 0;
};

class I2class: public I1class{
    double getI(){
        return 2;
    }
};

class J1class{
    int i;
    int j;
    class J2class{
        int i;
        int j;
        int J2test(int a, int b);
    };
};

int J1class::J2class::J2test(int a, int b){
    a = 0;
    return b;
}

int main(){
    cout<<"HI"<<endl;
    return 0;
}