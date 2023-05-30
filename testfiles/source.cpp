// #include <iostream>
// using namespace std;

int sum (int x, int y){
	return x+y; 
}
int sum(int &x, int y){
	return x+y;
}

int main(){
	int x;
	cin >> x;
	cout <<"Source";
	cout <<"YES";
	return 0;
}