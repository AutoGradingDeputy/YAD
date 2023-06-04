# Isolator

## What is Isolator? 
Isolator tool isolates the whole code from a given function or class inside destination code and replaces the isolated function or class from source code inside destination code.
It consists of two parts, IsolateFunction and IsolateClass.

## Commands:
### Isolate Function
` isolate f source.cpp destination.cpp "function prototype" ` 
### Isolate Class 
` isolate c source.cpp destination.cpp "class  class-name" `

By default, it only isolates the class with its member functions' implementation. Adding the option '-all' gives more options: 

- Isolates the class with all its dependent classes (inherited classes and friend classes). 
`isolate c source.cpp destination.cpp "class  class-name" -all t`

- Isolates the class definition only.
`isolate c source.cpp destination.cpp "class  class-name" -all c`

## How does it work?
Isolator will search for the desired function\class inside source.cpp and take a copy of it, after that it will search for the desired function\class inside destination.cpp and inserts it in the appropriate place as described below.
Searching for a function or class depends on signature matching. 
    
## Where it will be inserted? 
### <strong> Isolate fucntion: </strong>

<strong> Non-member function: </strong>

Function's prototype will be inserted in the beginnig of the code, and function's implementation will be inserted at the end of the code.

<strong> Member function: </strong>

- The orginal function is implemented inside the class: 

    Function will be inserted at the end of the class.

- The orginal function is implemented inside the class: 

    Function's prototype will be inserted at the end of the class, and function's implementation will be inserted at the end of the code.

### <strong> Isolate Class:</strong>
<strong> Class found in destination code: </strong>
    
Original class will be commented and the copied class from source.cpp will be pasted in the exact place of the original class in detination.cpp

<strong> Class not found in destination.cpp: </strong>
    
The copied class from source.cpp will be pasted at the end of detination.cpp 


## Error Scenarios:
<strong> The following cases outputs an error message </strong>

### Isolate Function:
<strong> Non-member Functions: </strong> 

- Function doesn't exist in source.cpp 

<strong> Member Functions: </strong>

- Parent Class doesn't exist in destination.cpp

- Function doesn't exist in source.cpp 


### Isolate Class:
<strong> Class: </strong>

- Class doesn't exist in source.cpp 

<strong> Struct: </strong>

- Struct doesn't exist in source.cpp 

<div class="bs-callout bs-callout-info">
    <h4> Note </h4>
    While isolating a member function, writing the class on one lines results with errors.
    Please write the class on at least 2 lines.
    Write the class on 2 lines or more inside your .cpp file
    <div class="bs-callout bs-callout-danger">
        <code>
        <strong> DON'T: </strong> </br>
        class x{}
        </code>
    </div>
    <div class="bs-callout bs-callout-success">
        <code style="color:green;"> 
        <strong > DO: </strong> </br>
        class x{ 
        </br> }
        </code>
    </div>
</div>

For reference on how to write functions' parameters, please check [the reference page](./reference.md)
