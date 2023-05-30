// #include <iosatrem>
// using namespace std;


int main(){
	cout <<"Destination";
	book b1;
	b1.sum(5);
	return 0;
}

class A{
	template <typename T> T myMax(T &x, T y);
};
class B{
 friend class A;
};
class Animal {
	public:
	void eat() {
	cout << "Animal is eating." << endl;
	}
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
	int sum(int y, int z);
int Animal :: sum(int y, int z){
	return y+z;
}
class Dog : public Animal {
	public:
	void bark() {
	cout << "Dog is barking." << endl;
	}
};
