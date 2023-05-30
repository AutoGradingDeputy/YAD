# References
Below are examples of how to write the function's parameter

<strong> Non-member Functions: </strong> 

- Normal Function: simply write the function prototype, such as: 
    - `"int sum(int , int)"`
- Template Function write the function prototype along with the template definition:
    - `"template <typename T> T myMax1(T &, T)"`
- Function with array parameter: 
    - `"int print_array(int size, int a *)"`

<strong> Member Functions: </strong>

- Normal & Template Fucntions: 
    - You need to add the name of the parent class:
        - `"template <typename T> T MyClass:: myMax2(T &, T)"`
        - `"void MyClass:: print()"` 
- Static: 
    - Write the static key word at the beginning of the prototype:
        - `"static void MyClass::eat()"`
- const: 
    - `"double MyClass:: getArea() const"` 
- virtual: 
    - `"virtual double MyClass:: getArea() const"`
- pure virtual:
    - `"virtual double MyClass:: getArea() const = 0"` 
- constructor: 
    - `"MyClass :: MyClass()"`
- initiaizer list:
    - `"MyClass :: MyClass(int, double, char) : myInt()"`
- copy constructor: 
    - `"MyClass :: MyClass(const MyClass&)"`
- destructor: 
    - `"MyClass :: ~MyClass()"`
