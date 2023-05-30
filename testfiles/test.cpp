// #include <iostream>
// using namespace std;

class MyClass {
    private:
        int myInt;
        double myDouble;
        char myChar;
    public:
        MyClass(int i, double d, char c) : myInt(i), myDouble(d), myChar(c) {
        
        }
        MyClass(){
            myChar = 'a';
            myDouble=0;
            myInt=0;
        }
        MyClass(const MyClass& other) : data(new int(*other.data)) {
            std::cout << "Copy constructor called" << std::endl;
        }
        ~MyClass(){

        }
};

template <typename T> T myMax1(T &x, T y){
  cout<<"Please"<<endl;


  T bb;
}

int ss(int y){
	return 1+y;
}

struct Node{
	int y;
	int x;
};
class A{
    template <typename T> T myMax(T &x, T y);
    template <typename T> T myMax2(T &x, T y){
        cout <<" TEST";
    };
};
template <typename T> T A ::  myMax(T &x, T y){
   cout<<"Please"<<endl;


   T bb;
}
class B{
friend class A;
};
class Animal {
	public:
	static void eat();
	void print() const;
	private:
		int x;
	public:
	int y;
	int sum(int x){
		return x+5;
	}
	friend class A;
	int sum(int y, int z);
	
};
static void Animal :: eat(){
	cout << "Animal is eating." << endl;
}
int sum1(int x, int y){
	return x+y;
}
int Animal :: sum(int y, int z){
	return y+z;
}
int testing(int x){
	return x+1;
}
class Dog : public Animal {
	public:
	void bark() {
	cout << "Dog is barking." << endl;
	}
};
class Shape {
	friend class Animal;
	friend int testing( int x);
	public:
		virtual double getArea() const = 0;
};

class Rectangle : public Shape {
	public:
		Rectangle(double width, double height) : width_(width), height_(height) {}
		int rec1( int x );
		double getArea() const override {
			return width_ * height_;
		}

	private:
		double width_;
		double height_;
};

int main(){
	int y=0;
	cout << y;
}

int Rectangle :: rec1(int x ){
	return x*6;
}