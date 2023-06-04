# CommentController

## Whats CommentController:
CommentControl tool allows the user to control comments by extracting or removing comments, or by commenting out certain classes or functions.

## Commands:
### Extract Comments:
This tool will extract all the comments from a C++ file and output the comments.

`commentCtrl e source.cpp`

### Extract Header:
This tool will extract all header comments from a C++ file and output the comments.

`commentCtrl h source.cpp`

### Delete Comments:
This tool will delete all the comments from a .cpp or .h file and output the source code.

`commentCtrl d source.cpp`

### Comment Out Function:
This tool will comment out a function implementation from a C++ file using a function prototype and output the new code.

`commentCtrl f source.cpp "function prototype"`

### Comment Out Class:
This tool will comment out a Class implementation from a C++ file and output the new code.

`commentCtrl c source.cpp "class class-name"`

By default, it only comments the class with its member functions' implementation. Adding the option '-all' gives more options: 

- Comments the class with all its dependent classes (inherited classes and friend classes). 
`commentCtrl c source.cpp "class  class-name" -all t`

- Comments the class definition only.
`commentCtrl c source.cpp "class  class-name" -all c`

## Output options
<strong> -o </strong> followed by the path of the file you want the output to be saved in (The default is printing the output on the terminal).

### Example command with option:
- Write on a new file:
`commentCtrl d source.cpp -o new.cpp`
  
- Write on the same file
`commentCtrl d source.cpp -o source.cpp`

For reference on how to write functions' parameters, please check [the reference page](./reference.md)