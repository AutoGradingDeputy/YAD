import typer
import re
import codeParser

app = typer.Typer()

#This function is responsible for converting classes and functions to comments in a .cpp or .h file
def commentMaker(source: str, type: str, name: str, isolate =0, option=0, output = ""):

    #Find where the classes or functions start
    position = codeParser.positions(source, type , name, option, False)
    if position == ["error"]:
        return
    if position == []:
        if isolate == 0:
            print("NOT FOUND")
        return
    
    num = len(position)
    
    #Get all the code to edit it
    with open(source, 'r') as f:
        lines = f.readlines()
        
    for i in range(0, int(num), 4):
        lines[position[i]-1] = "//" + lines[position[i]-1]
        for line in range(position[i], position[i+1]):
            lines[line] = "//" + lines[line]
    
    
    #Write the modified code into the file.
    if output != "":
        with open(output, 'w') as f:
            f.writelines(lines)
    else:
        for line in lines:
            print(line)



#This function is responsible for removing all comments from a .cpp or .h file
@app.command("d")
def deleteComments(source: str  = typer.Argument(..., help="The path of the .cpp or .h file the user wants delete comments to work on."),
                    output: str  = typer.Option("", "-o", help="The path of the .cpp or .h file the user wants the output to be saved in (Default is printing on the terminal).")):
    """
    This tool will delete all the comments from a .cpp or .h file and output the source code into the file of your choosing.
    """
    with open(source, 'r') as f:
        source = f.read()
    
    # Remove all comments from the input file
    source = re.sub(r'\/\/.*?$|\/\*[\s\S]*?\*\/', '', source, flags=re.MULTILINE)

    # Write the modified contents to the output file
    if output != "":
        with open(output, 'w') as f:
            f.write(source)
    else:
        print(source)



#This function is responsible for extracting all comments from a .cpp or .h file into a file or to print on the terminal
@app.command("e")
def extractComments(source: str  = typer.Argument(..., help="The path of the .cpp or .h file the user wants extracts comments to work on."),
                    output: str  = typer.Option("", "-o", help="The path of the .cpp or .h file the user wants the output to be saved in (Default is printing on the terminal).")):
    """
    This tool will extract all the comments from a C++ file and output the comments into the file of your choosing.
    """
    with open(source, 'r') as f:
        source = f.read()
    
    # Extract all comments from the input file
    comments = re.findall(r'\/\/.*?$|\/\*[\s\S]*?\*\/', source, flags=re.MULTILINE)

    # Write the comments to the output file or to the terminal
    if output != "":
        with open(output, 'w') as f:
            for comment in comments:
                size = len(comment)
                if comment[0:2] == "/*":
                    comment = comment[2:size-2].strip()
                else:
                    comment = comment[2:size].strip()
                f.write(comment + "\n")
    else:
        for comment in comments:
            print(comment)



#This function is responsible for extracting all header comments from a .cpp or .h file into a file or to print on the terminal
@app.command("h")
def extractHeader(input: str  = typer.Argument(..., help="The path of the .cpp or .h file the user wants extracts header comments to work on."),
                   output: str  = typer.Option("", "-o", help="The path of the .cpp or .h file the user wants the output to be saved in (Default is printing on the terminal).")):
    """
    This tool will extract all header comments from a C++ file and output the comments into the file of your choosing.
    """
    with open(input, 'r') as f:
        source = f.read()

    #Find all header comments
    header = re.findall(r'\/\/.*?$|\/\*[\s\S]*?\*\/', source, flags=re.MULTILINE)
    amount = 0

    while source[0:1] == '\n':
        source = source[1:]

    while source[0:2] == "//" or source[0:2] == "/*":
        source = re.sub(r'\/\/.*?$|\/\*[\s\S]*?\*\/', '',source, flags=re.MULTILINE, count=1)
        amount += 1
        while source[0:1] == '\n':
            source = source[1:]

    # Write the header comments to the output file
    if output != "":
        with open(output, 'w') as f:
            for n in range(amount):
                comment = header[n]
                size = len(comment)
                if comment[0:2] == "/*":
                    comment = comment[2:size-2]
                else:
                    comment = comment[2:size]
                f.write(comment + "\n")
    else:
        for n in range(amount):
            comment = header[n]
            print(comment)



#This function is responsible for commenting out classes specified by the user from a .cpp or .h file
@app.command("c")
def CommentOutClass(
    source: str  = typer.Argument(..., help="The path of the .cpp or .h file the user wants comment out class to work on."),
    prototype: str  = typer.Argument(..., help="The class the user wants to check (Must input like this: \"class name\")."),
    all: str  = typer.Option("true", "-all", help="If true this will isolate the class with all its children classes"),
    isolate: int = typer.Argument(0, hidden=True, help="A hidden variable for developers' use, used to show that function was called by isolator."),
    output: str  = typer.Option("", "-o", help="The path of the .cpp or .h file the user wants the output to be saved in (Default is printing on the terminal).")):
    """
    This tool will comment out a class implementation from a C++ file using a class prototype (equivalent to deleting the class).
    """
    if all.lower() not in ["true","false"]:
        print("Invalid input for -all")
        return False
    
    type = prototype.split(" ")[0]
    option = 1
    if all.lower() == "true":
        option = 0

    commentMaker(source, type , prototype, isolate, option, output)



#This function is responsible for commenting out functions specified by the user from a .cpp or .h file
@app.command("f")
def CommentOutFunction(
    source: str  = typer.Argument(..., help="The path of the .cpp or .h file the user wants comment out class to work on."),
    prototype: str  = typer.Argument(..., help="The function the user wants to check (Must input like this: \"int functionName(int, int)\"."),
    isolate: int = typer.Argument(0, hidden=True, help="A hidden variable for developers' use, used to show that function was called by isolator."),
    output: str  = typer.Option("", "-o", help="The path of the .cpp or .h file the user wants the output to be saved in (Default is printing on the terminal).")):
    """
    This tool will comment out a function implementation from a C++ file using a function prototype (equivalent to deleting the function).
    """
    commentMaker(source, "function" , prototype, isolate, 0, output)



#This function comments out all includes and using namespaces, this is needed to make libclang work properly
def includePreparer(input: str):

    with open(input, 'r') as f:
        source = f.read()

    source = re.sub(r'^#include\s*[\s\S][<"]\S+[>"]$', r'// \g<0>', source, flags=re.MULTILINE)
    source = re.sub(r'^\s*using\s+namespace\s+\S+;$', r'// \g<0>', source, flags=re.MULTILINE)

    with open(input, 'w') as f:
        f.write(source)



#This function comments out all includes and using namespaces, this is needed to make libclang work properly
def includeRevert(input: str):

    with open(input, 'r') as f:
        source = f.read()

    source = re.sub(r'^//\s*#include\s*', r'#include ', source, flags=re.MULTILINE)
    source = re.sub(r'^\s*//\s*using\s+namespace\s*', r'using namespace ', source, flags=re.MULTILINE)

    with open(input, 'w') as f:
        f.write(source)



if __name__ == "__main__":
    app()
