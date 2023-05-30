#include <iostream>
using namespace std;

class testf{
    friend double ** gettest();
    template <typename T> friend T myMax(T &x, T y);
    friend int testfunc(int &a, int b);
    public:
    virtual void show() = 0;
};

class testg: public testf{
    public:
    void show();
};

void testg::show(){
    cout<<"hi"<<endl;
}

class testb;

class testd{
    //friend class testc;
    int pleasework() const{
    
    }
    template <typename T> static int stattest2(T t);
};
template <typename T> int testd::stattest2(T t){

}

template <typename T> static int stattest3(T t){

}

class testb{
    class testd{
        ~testd(){
            cout<<"Hi";
        }
    };
    testb(int a, int b, int c);
    ~testb();
    testb(testb &t);
};

testb::testb(int a, int b, int c){
    cout<<"HI"<<endl;
}

testb::testb(testb &t){

}

testb::~testb(){
}

class testc{
    private: 
    static int testfunc(int a);
    int testfunc(int a){
        //hi how r u
        return 0;
    }
    template <typename T> T myHi(T x, T y);
    
    
};
template <typename T> T testc::myHi(T x, T y){
    return 0;
    
}


class teste: private testc{

};

int testc::testfunc(int a){
    return 0;
}

int testfunc(int &a, int b){
   const int c = 0;
   return a + b;
   //do yo show ?
}

int testfunc(int a){
    return 0;
}

int main(){
    cout<<"Test"<<endl;
    return 0;
}

double ** gettest(){
    return 0;
}

template <typename T> T myMax(T &x, T y){
    cout<<"Please"<<endl;


    T bb;
}

int hi();

int hi(){
    return 0;
}
static int stattest();

static int stattest(){
    return 0;
}

class testh{
    int testconst() const;
    int testconst2(){
        
    }
};

int testh::testconst() const{
    return 0;
}


class AB {
public:
  void sound(){
    cout <<"MEOW";
  }
};

class D2 : private AB {
  void g(){
    cout <<"G";
  }
  void sound(){
    cout <<"DDD";
  }
};