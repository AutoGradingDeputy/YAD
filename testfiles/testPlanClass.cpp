#include <iostream>
#include <algorithm>
using namespace std;

class Aclass{
    private:
    int i;
    int j;
    int Atest(int , double){
        
        return 0;
    }
    int fib(int x){
        if ( x== 1 ) return 1;
        return x;
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

int Eclass::Etest(int a,int b){
    return 0;
}

class Fclass{
    private:
    int i;
    int j;
    
    Fclass(){
        i = 0;
        j = 1;
    }
    Fclass(Fclass &a);
    ~Fclass();
};

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

class Kclass{
    int functionA(int a, int b) const{
        return a+b;
    }
    virtual void functionB() = 0;
    static int functionC(int a, int b);
    int functionD(int a, int b);
};
int Kclass :: functionD(int a, int b){
    cout << a <<" "<< b;
    return 1;
}

template <class K, class V>
class Lclass {
public:
    K key;
    V value;

};

struct Mclass{
	int y;
	int x;
	void print();
};
void Mclass :: print(){
    cout<<"Struct here";
}
struct M2class{
    friend class Mclass;
    double getM(){
        return 2;
    }
};

class myClass {
    private:
        int myInt;
        double myDouble;
        char myChar;
        string data;
        static void eat();
        void print() const;
        virtual double getArea1() const = 0;
        virtual double getArea() const{
            return myInt*myDouble;
        };
    public:
        myClass(int i, double d, char c) : myInt(i), myDouble(d), myChar(c) {
        
        }
        myClass(){
            myChar = 'a';
            myDouble=0;
            myInt=0;
        }
        myClass(const myClass& other){
            std::cout << "Copy constructor called" << std::endl;
        }
        ~myClass(){

        }
        template <typename T> T myMax(T &x, T y);
        template <typename T> T myMax2(T &x, T y){
            cout <<" TEST";
        };
        int sum(int x, int y);
};
class myClass1 : public myClass {
	public:
		myClass1(double width, double height) : width_(width), height_(height) {}
		int rec1( int x );
		double getArea() const override {
			return width_ * height_;
		}

	private:
		double width_;
		double height_;
};
void myClass :: print() const{
    cout << "testing const";
}
int myClass :: sum(int x, int y){
    return x+y;
}
template <typename T> T myClass ::  myMax(T &x, T y){
   cout<<"Please"<<endl;


   T bb;
}
int main(){
    cout << "YES";
    return 0;
}