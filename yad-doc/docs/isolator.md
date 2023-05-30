# Isolator

## What is Isolator? 
Isolator tool isolates the whole code from a given function or class inside destination code and replaces the isolated function or class from source code inside destination code.
It consists of two parts, IsolateFunction and IsolateClass.

## Commands:
### Isolate Function
` isolate f source.cpp destination.cpp "function prototype" ` 
### Isolate Class 
` isolate c source.cpp destination.cpp "class  class-name" `

By default, it only isolates the class with its member functions. Adding the option '-all' also isolates all its dependent classes:

` isolate c source.cpp destination.cpp "class  class-name" -all True`

## How does it work?
First of all the desired function\class must have the same signature in both source and destination files, then Isolator will search for the desired function\class inside source.cpp and take a copy of it, after that it will search for the desired function\class inside destination.cpp.
    
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
    Write the class on 2 lines or more inside your .cpp file
    <div class="bs-callout bs-callout-danger">
        <code>
        class x{}
        </code>
    </div>
    <div class="bs-callout bs-callout-success">
        <code> class x{ 
        </br> }
        </code>
    </div>
</div>

For reference on how to write functions' parameters, please check [the reference page](./reference.md)
