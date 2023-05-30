import yaml
import json
import typer
import re
import codeParser
import commentController

app = typer.Typer()

#Returns everything in the scope the user defined
def scopeGetter(source:str, scope:str ):
    #Checks if scope for function or class
    type = scope.split(" ")[0]
    if type != "class":
        type = "function"
    
    #Find where function or class is
    pos = codeParser.positions(source, type, scope, True)
    if pos == ["error"]:
        return ["error"]
    if pos == []:
        print("Warning: " + type + " doesn't exist in " + source +" file")
        return ["error"]
    searchPos = []
    count = 0

    for p in pos:
        if count != 2 and count != 3:
            searchPos.append(p)
            count += 1
        elif count == 2:
            count += 1
        else:
            count = 0

    #Get back only the lines in the specified scope
    with open(source, 'r') as f:
        source = f.readlines()
    scopeLines = []
    i = 0
    while i < len(searchPos):
        j = searchPos[i] - 1
        while j < searchPos[i+1]:
            scopeLines.append(source[j])
            j += 1
        i += 2

    source = '\n'.join(scopeLines)
    return source



#Function that uses all other restriction functions that are below it, it recieves a YAML file which lets it know which functions to run
@app.command("r")
def restrict(source: str  = typer.Argument(..., help="The path of the .cpp or .h file the user wants restrictor to work on."),
             rules: str  = typer.Argument(..., help="The path of the YAML file containing user requirements."),
             output: str  = typer.Option("n", "-o", help="If n this will make restrict print the number of violations, Input V if you want a list of violations to be printed and more information (default is n) (Takes only V or n or N)."),
             hide: bool = typer.Argument(False, hidden=True, help="A hidden variable for developers use, used with checkAPI to show the names of the functions or classes that are violating the YAML file (extra)."),
             hide2: bool = typer.Argument(False, hidden=True, help="A hidden variable for developers use, used to show that checkAPI called restrict")):
    """
    This tool will recieve a YAML file made by the user and restrict a .cpp or .h file according to that YAML file, it will return a list of findings (for YAML file explanation check GitHub).
    """
    #Used to control the style of output
    if output not in ["n", "N", "V", "v"]:
        print("Invalid -o input")
        return False
    
    outputBool = False
    if output == "n" or output == "N":
        outputBool = True

    with open(rules) as file:
        yamlFile = yaml.load(file, Loader=yaml.FullLoader)
    jsonFormat = json.dumps(yamlFile, indent=4)
    jsonData = json.loads(jsonFormat)

    #Used to remove comments from file, important for all restrictors (library only one that needs to work without it)
    newSource = "commentDeletedFileForRestrictor.cpp"
    commentController.deleteComments(source, newSource)

    #Following variables are needed to print everything in a readable manner for the user and for the loop to function correctly
    critOld = "start"
    critAns = True
    exactCount = 0
    compareCount = 0
    parentCheck = []
    violationCount = 0

    for criteria, critData in jsonData.items():
        #The following code is to print the findings of the code for each criteria in the YAML file
        if critOld != "start":
            if exactCount != 0 and compareCount != exactCount:
                critAns = critAns & False
            # if critData['restriction'].lower() == 'exactly' and not critAns and not outputBool and not hide:
            #     print(critOld + " are not exactly the same.")
            critAns = True
            compareCount = 0
            exactCount = 0

        critOld = criteria

        #Handles libraries in YAML file
        if criteria == 'libraries':
            for lib in critData['names']:
                if critData['restriction'].lower() != 'exactly':
                    if not libRestrict(source, critData['restriction'], lib, True):
                        critAns = False
                        violationCount += 1
                        if not outputBool:
                            if critData['restriction'].lower() == "forbidden":
                                print("Violating library: " + lib)
                            elif not hide:
                                print("Missing library: " + lib)
                            else:
                                print("Extra library: " + lib)
                else:
                    if not libRestrict(source, 'at_least', lib, True):
                        critAns = False
                        violationCount += 1
                        if not outputBool:
                            if not hide:
                                print("Missing library: " + lib)
                            else:
                                print("Extra library: " + lib)
                    exactCount += 1
                    if exactCount == 1:
                        with open(source, 'r') as f:
                            data = f.read()
                        compareCount =  len(re.findall(r'^#include\s*[\s\S][<"]\S+[>"]$', data, flags=re.MULTILINE))

        #Handles keywords in YAML file
        elif criteria == 'keywords':
            keyCount = True
            for kword in critData['names']:
                if critData['restriction'].lower() != 'exactly':
                    if not wordRestrict(newSource, critData['restriction'], kword, critData['scope'], True):
                        critAns = False
                        violationCount += 1
                        if not outputBool:
                            if critData['restriction'].lower() == "forbidden":
                                print("Violating keyword: " + kword)
                            elif not hide:
                                print("Missing keyword: " + kword)
                            else:
                                print("Extra keyword: " + kword)
                else:
                    if keyCount:
                        print("exactly not supported for keywords, at_least will be used instead.")
                        keyCount = False
                    if not wordRestrict(newSource, 'at_least', kword, critData['scope'], True):
                        critAns = False
                        violationCount += 1
                        if not outputBool:
                            if not hide:
                                print("Missing keyword: " + kword)
                            else:
                                print("Extra keyword: " + kword)

        #Handles classes in YAML file
        elif criteria == 'classes':
            for cls in critData['names']:
                if critData['restriction'].lower() != 'exactly':
                    if not classRestrict(newSource, critData['restriction'], cls, critData['scope'], True):
                        if len(cls.split("::")) != 1:
                            continue
                        critAns = False
                        violationCount += 1
                        if not outputBool:
                            if critData['restriction'].lower() == "forbidden":
                                print("Violating class: " + cls)
                            elif not hide:
                                print("Missing class: " + cls)
                            else:
                                print("Extra class: " + cls)
                else:
                    if len(cls.split("::")) != 1:
                            continue
                    if not classRestrict(newSource, 'at_least', cls, critData['scope'], True):
                        critAns = False
                        violationCount += 1
                        if not outputBool:
                            if not hide:
                                print("Missing class: " + cls)
                            else:
                                print("Extra class: " + cls)
                    exactCount += 1
                    if exactCount == 1:
                        if critData['scope'].lower() == "global" or critData['scope'] == "":
                            data = codeParser.prepareData(newSource, True)
                            if data == ["error"]:
                                return False
                        else:
                            scopeG = scopeGetter(newSource, critData['scope'])
                            file = open("restrictorGen.cpp", "w")
                            file.write(scopeG)
                            file.close()
                            data = codeParser.prepareData("restrictorGen.cpp", True)
                            if data == ["error"]:
                                return False
                        for decl in data['nodes']:
                            if decl['kind'] == "CLASS_DECL" and decl['start'] != decl['end']:
                                compareCount += 1

        #Handles functions in YAML file
        elif criteria == 'functions':
            for func in critData['names']:
                if critData['restriction'].lower() != 'exactly':
                    if not funcRestrict(newSource, critData['restriction'], func, critData['scope'], True):
                        critAns = False
                        violationCount += 1
                        if not outputBool:
                            if critData['restriction'].lower() == "forbidden":
                                print("Violating function: " + func)
                            elif not hide:
                                print("Missing function: " + func)
                            else:
                                print("Extra function: " + func)
                else:
                    if not funcRestrict(newSource, 'at_least', func, critData['scope'], True):
                        critAns = False
                        violationCount += 1
                        if not outputBool:
                            if not hide:
                                print("Missing function: " + func)
                            else:
                                print("Extra function: " + func)
                    exactCount += 1
                    if exactCount == 1:
                        if critData['scope'].lower() == "global" or critData['scope'] == "":
                             data = codeParser.prepareData(newSource, True)
                             if data == ["error"]:
                                return False
                        else:
                            scopeG = scopeGetter(newSource, critData['scope'])
                            file = open("restrictorGen.cpp", "w")
                            file.write(scopeG)
                            file.close()
                            data = codeParser.prepareData("restrictorGen.cpp", True)
                            if data == ["error"]:
                                return False
                        for decl in data['nodes']:
                            if decl['kind'] == "FUNCTION_DECL" and decl['start'] != decl['end']:
                                compareCount += 1

        #Handles (private/public/protected) functions in YAML file
        elif criteria == 'private_functions' or criteria == 'public_functions' or criteria == 'protected_functions':
            access = criteria.split("_")[0].upper()
            for func in critData['names']:
                if critData['restriction'].lower() != 'exactly':
                    if not accessRestrict(newSource, critData['restriction'], func, critData['scope'], access, True):
                        critAns = False
                        violationCount += 1
                        if not outputBool:
                            if critData['restriction'] == "forbidden":
                                print("Violating " + access + " function: " + func)
                            elif not hide:
                                print("Missing " + access + " function: " + func)
                            else:
                                print("Extra " + access + " function: " + func)
                else:
                    if not accessRestrict(newSource, 'at_least', func, critData['scope'], access, True):
                        critAns = False
                        violationCount += 1
                        if not outputBool:
                            if not hide:
                                print("Missing " + access + " function: " + func)
                            else:
                                print("Extra " + access + " function: " + func)
                    exactCount += 1
                    if exactCount == 1:
                        if critData['scope'].lower() == "global" or critData['scope'] == "":
                             data = codeParser.prepareData(newSource, True)
                             if data == ["error"]:
                                return False
                        else:
                            scopeG = scopeGetter(newSource, critData['scope'])
                            file = open("restrictorGen.cpp", "w")
                            file.write(scopeG)
                            file.close()
                            data = codeParser.prepareData("restrictorGen.cpp", True)
                            if data == ["error"]:
                                return False
                        for decl in data['nodes']:
                            if decl['kind'] == "CXX_METHOD" and decl['access_type'] == access and (decl['start'] != decl['end'] or decl['is_virtual_method'] == True):
                                if decl['is_virtual_method'] == True:
                                    if decl['parent_class'] in parentCheck:
                                        compareCount -= 1
                                    parentCheck.append(decl['parent_class'])
                                compareCount += 1
    

    #To print the last criteria in the loop
    if exactCount != 0 and compareCount != exactCount:
        critAns = critAns & False
    # if critData['restriction'].lower() == "exactly" and not critAns and not outputBool and not hide:
    #     print(critOld + " are not exactly the same.")
    if outputBool:
        print(violationCount)
    



#Function to restrict a single library, no need for the YAML file, further explanation available exactly below function definition
@app.command("l")
def libRestrict(source: str  = typer.Argument(..., help="The path of the .cpp or .h file the user wants restrictor to work on."),
                 restriction: str = typer.Argument(..., help="The restriction type used for 3 ways of checking:\n\nat_least: The library being checked must exist (It can be with other libraries).\n\nexactly: The library being checked must only exist (It can not be with other libraries).\n\nforbidden: The library being checked must not exist."),
                 lib: str = typer.Argument(..., help="The name of the library the user wants to check (only input the name of the library without #include)."),
                 hide:bool = typer.Argument(False, hidden=True, help="A hidden variable for developers use, used to return boolean")):
    """
    This tool will check if a certain library inputted by the user follows as certain restriction type of (at_least/exactly/forbidden) in a .cpp or .h file also inputted by the user.
    """

    #Makes sure that restriction inputted is a viable restriction
    if restriction.lower() not in ["exactly", "forbidden", "at_least"]:
        print("Invalid Restriction Input")
        return False
    
    with open(source, 'r') as f:
        source = f.read()

    #Handles restriction type "exactly"
    if restriction.lower() == "exactly":
        header = re.findall(r'^#include\s*[\s\S][<"]\S+[>"]$', source, flags=re.MULTILINE)
        if len(header) == 1:
            header = header[0].split("<")[1].split(">")[0] if len(header[0].split("<")) > 1 else header[0].split("\"")[1]
            if header == lib:
                if hide == False:
                    print("True")
                return True
            else:
                if hide == False:
                    print("False")
                return False

    #Handles restriction types "at_least" and "forbidden"
    else:
        existFlag = False
        header = re.findall(r'^#include\s*[\s\S][<"]\S+[>"]$', source, flags=re.MULTILINE)
        lib1 = "#include<" + lib + ">"
        lib2 = "#include\""+ lib + "\""

        for library in header:
            library = library.replace(" ","")
            if library == lib1 or library == lib2:
                existFlag = True

        if restriction.lower() == "forbidden":
            if existFlag == False:
                if not hide:
                    print("True")
                return True
            else:
                if not hide:
                    print("False")
                return False
        elif restriction.lower() == "at_least":
            if existFlag == True:
                if not hide:
                    print("True")
                return True
            else:
                if not hide:
                    print("False")
                return False



#Function to restrict a single keyword, no need for the YAML file, further explanation available exactly below function definition.
@app.command("k")
def wordRestrict(source: str  = typer.Argument(..., help="The path of the .cpp or .h file the user wants restrictor to work on."),
                 restriction: str = typer.Argument(..., help="The restriction type used for 2 ways of checking:\n\nat_least: The keyword being checked must exist (It can be with other keywords).\n\nforbidden: The keyword being checked must not exist.\n\nexactly not available for keywords, will work as at_least."),
                 keyword: str = typer.Argument(..., help="The keyword the user wants to check (This function matches using regex, function prototypes don't work here, must input exactly what you want to match)."),
                 scope: str = typer.Argument(..., help="The scope the user wants to check inside (Function or Class, use their prototypes)."),
                 hide:bool = typer.Argument(False, hidden=True, help="A hidden variable for developers use, used to return boolean")):
    """
    This tool will check if a certain keyword inputted by the user follows as certain restriction type of (at_least/exactly/forbidden) in a .cpp or .h file also inputted by the user.
    """

    #Makes sure that restriction inputted is a viable restriction
    if restriction.lower() not in ["exactly", "forbidden", "at_least"]:
        print("Invalid Restriction Input")
        return False
    
    #Check if global scope or not, if not then use scopeGetter to get everything in the scope defined by the user
    if scope.lower() == "global" or scope == "":
        with open(source, 'r') as f:
            source = f.read()
    else:
        source = scopeGetter(source, scope)
        if source == ["error"]:
            return False
    
    #Check if keyword exists and print true or false according to restriction
    if re.search(fr"(?i).*return\s*[^\n;]+{re.escape(keyword)}.*", source):
        if restriction.lower() == "at_least" or restriction.lower() == "exactly":
            if not hide:
                print("True")
            return True
        elif restriction.lower() == "forbidden":
            if not hide:
                print("False")
            return False
    else:
        if restriction.lower() == "at_least" or restriction.lower() == "exactly":
            if not hide:
                print("False")
            return False
        elif restriction.lower() == "forbidden":
            if not hide:
                print("True")
            return True



#Function to restrict a single class, no need for the YAML file, further explanation available exactly below function definition.
@app.command("c")
def classRestrict(source: str  = typer.Argument(..., help="The path of the .cpp or .h file the user wants restrictor to work on."),
                 restriction: str = typer.Argument(..., help="The restriction type used for 3 ways of checking:\n\nat_least: The class being checked must exist (It can be with other classes).\n\nexactly: The class being checked must only exist (It can not be with other classes).\n\nforbidden: The class being checked must not exist."),
                 prototype: str = typer.Argument(..., help="The class the user wants to check (Must input like this: \"class name\")."),
                 scope: str = typer.Argument(..., help="The scope the user wants to check inside (Function or Class, input their prototypes)."),
                 hide:bool = typer.Argument(False, hidden=True, help="A hidden variable for developers use, used to return boolean")):
    """
    This tool will check if a certain class inputted by the user follows as certain restriction type of (at_least/exactly/forbidden) in a .cpp or .h file also inputted by the user.
    """

    #Makes sure that restriction inputted is a viable restriction
    if restriction.lower() not in ["exactly", "forbidden", "at_least"]:
        print("Invalid Restriction Input")
        return False
    
    #Check if global scope or not, if not then use scopeGetter to get everything in the scope defined by the user
    if scope.lower() == "global" or scope == "":
        data = codeParser.prepareData(source, True)
        if data == ["error"]:
            return False
        with open(source, 'r') as f:
            scopeG = f.read()
    else:
        scopeG = scopeGetter(source, scope)
        if scopeG == ["error"]:
            return False
        file = open("restrictorGen.cpp", "w")
        file.write(scopeG)
        file.close()
        data = codeParser.prepareData("restrictorGen.cpp", False)
        if data == ["error"]:
            return False

    prototype = prototype.strip()
    empty = []
    #Check if class exists and print true or false according to restriction
    if codeParser.findLocationClass(data, prototype, source, "class") != empty:
        if restriction.lower() == "exactly":
            if len(re.findall(r"(?:(?<=\s)|(?<=^))class.*?\{(?=\s|$)", scopeG, flags=re.MULTILINE)) > 1:
                if not hide:
                    print("False")
                return False
            else:
                if not hide:
                    print("True")
                return True
        elif restriction.lower() == "at_least":
            if not hide:
                print("True")
            return True
        elif restriction.lower() == "forbidden":
            if not hide:
                print("False")
            return False
    else:
        if restriction.lower() == "at_least" or restriction.lower() == "exactly":
            if not hide:
                print("False")
            return False
        elif restriction.lower() == "forbidden":
            if not hide:
                print("True")
            return True



#Function to restrict a single function, no need for the YAML file, further explanation available exactly below function definition.
@app.command("f")
def funcRestrict(source: str  = typer.Argument(..., help="The path of the .cpp or .h file the user wants restrictor to work on."),
                 restriction: str = typer.Argument(..., help="The restriction type used for 3 ways of checking:\n\nat_least: The function being checked must exist (It can be with other functions).\n\nexactly: The function being checked must only exist (It can not be with other functions).\n\nforbidden: The function being checked must not exist."),
                 prototype: str = typer.Argument(..., help="The function the user wants to check (Must input like this: \"int functionName(int, int)\"."),
                 scope: str = typer.Argument(..., help="The scope the user wants to check inside (Function or Class, input their prototypes)."),
                 hide:bool = typer.Argument(False, hidden=True, help="A hidden variable for developers use, used to return boolean")):
    """
    This tool will check if a certain function inputted by the user follows as certain restriction type of (at_least/exactly/forbidden) in a .cpp or .h file also inputted by the user.
    """

    #Makes sure that restriction inputted is a viable restriction
    if restriction.lower() not in ["exactly", "forbidden", "at_least"]:
        print("Invalid Restriction Input")
        return False
    
    #Check if global scope or not, if not then use scopeGetter to get everything in the scope defined by the user
    if scope.lower() == "global" or scope == "":
        data = codeParser.prepareData(source, True)
        if data == ["error"]:
            return False
        with open(source, 'r') as f:
            scopeG = f.read()
    else:
        scopeG = scopeGetter(source, scope)
        if scopeG == ["error"]:
            return False
        file = open("restrictorGen.cpp", "w")
        file.write(scopeG)
        file.close()
        data = codeParser.prepareData("restrictorGen.cpp", False)
        if data == ["error"]:
            return False

    empty = []
    #Check if function exists and print true or false according to restriction
    if codeParser.findLocationFunction(data, prototype, source) != empty:
        if restriction.lower() == "exactly":
            if len(re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)\s*\{[^{}]*\}", scopeG, flags=re.MULTILINE)) > 1:
                if not hide:
                    print("False")
                return False
            else:
                if not hide:
                    print("True")
                return True
        elif restriction.lower() == "at_least":
            if not hide:
                print("True")
            return True
        elif restriction.lower() == "forbidden":
            if not hide:
                print("False")
            return False
    else:
        if restriction.lower() == "at_least" or restriction.lower() == "exactly":
            if not hide:
                print("False")
            return False
        elif restriction.lower() == "forbidden":
            if not hide:
                print("True")
            return True



#Function to restrict a single (private/public/protected) function, no need for the YAML file, further explanation available exactly below function definition.
@app.command("a")
def accessRestrict(source: str  = typer.Argument(..., help="The path of the .cpp or .h file the user wants restrictor to work on."),
                 restriction: str = typer.Argument(..., help="The restriction type used for 3 ways of checking:\n\nat_least: The function being checked must exist (It can be with other functions).\n\nexactly: The function being checked must only exist (It can not be with other functions).\n\nforbidden: The function being checked must not exist."),
                 prototype: str = typer.Argument(..., help="The function the user wants to check (Must input like this: \"int functionName(int, int)\" or \"int functionName(int x,int y)\")."),
                 scope: str = typer.Argument(..., help="The scope the user wants to check inside (Function or Class, input their prototypes)."),
                 type: str = typer.Argument(..., help="The access type the user wants to check for (private/public/protected)."),
                 hide:bool = typer.Argument(False, hidden=True, help="A hidden variable for developers use, used to return boolean")):
    """
    This tool will check if a certain (private/public/protected) function inputted by the user follows as certain restriction type of (at_least/exactly/forbidden) in a .cpp or .h file also inputted by the user.
    """
    #Makes sure that restriction inputted is a viable restriction
    if restriction.lower() not in ["exactly", "forbidden", "at_least"]:
        print("Invalid Restriction Input")
        return False
    
    #Check if global scope or not, if not then use scopeGetter to get everything in the scope defined by the user as well as preparing data for access_type search
    if scope.lower() == "global" or scope == "":
        data = codeParser.prepareData(source, True)
        if data == ["error"]:
            return False
    else:
        scopeG = scopeGetter(source, scope)
        if scopeG == ["error"]:
            return False
        file = open("restrictorGen.cpp", "w")
        file.write(scopeG)
        file.close()
        data = codeParser.prepareData("restrictorGen.cpp", False)
        if data == ["error"]:
            return False

    #Variables used in the following if statement to find if function is private
    if len(prototype.split("virtual")) == 1 and len(prototype.split("static")) == 1:
        proto = prototype.split(' ')[0] + ' (' + prototype.split('(')[1].strip()
    else:
        proto = prototype.split(' ')[1] + ' (' + prototype.split('(')[1].strip()
    spelling = prototype.split('(')[0].split(' ')[-1].split('::')[-1]
    
    for decl in data['nodes']:
        if decl['kind'] == "CXX_METHOD" and decl['spelling'] == spelling and decl['prototype'].replace(" ","") == proto.replace(" ","") and decl['access_type'] == type.lower():
            return funcRestrict(source, restriction, prototype, scope, hide)
    if not hide:
        print("False")
    return False



#Function to restrict a single (private/public/protected) function, no need for the YAML file, further explanation available exactly below function definition.
def checkAPI(source: str  = typer.Argument(..., help="The path of the .cpp or .h file the user wants restrictor to work on."),
            restriction: str = typer.Argument(..., help="The restriction type used for 2 ways of checking:\n\nat_least: Everything being checked must exist (It can be with other functions/classes).\n\nexactly: Everything being checked must only exist (It can not be with other functions/classes)."),
            compare: str = typer.Argument(..., help="The path of the .cpp or .h file the user wants the source file to be compared to."),
            output: str  = typer.Option("n", "-o", help="If n this will make checkAPI print the number of missing functions/classes then extra functions/classes, Input V if you want a list of violations to be printed and more information (default is n) (Takes only v or V or n or N)."),
            hide:bool = typer.Argument(False, hidden=True, help="A hidden variable for developers use, used to return extra functions and classes found in the code.")):
    """
    This tool will compare two files together, the source and compare file, it will check if the function prototypes and class names match then return true or false accordingly.
    """
    #Used to control the style of output
    if output not in ["n", "N", "V", "v"]:
        print("Invalid -o input")
        return False

    data = codeParser.prepareData(compare, True)
    if data == ["error"]:
        return False

    #Makes sure that restriction inputted is a viable restriction
    if restriction.lower() not in ["exactly", "forbidden", "at_least"]:
        print("Invalid Restriction Input")
        return False
    
    #Varibales and loop used to create the YAML file needed to run restrictor, YAML file made from compare file.
    allPrivFunctions = []
    allPublicFunctions =[]
    allProtectedFunctions = []
    allFunctions = []
    allClasses = []
    virtual = ""
    const = ""
    unsigned = ""
    for decl in data['nodes']:
        if decl['prototype'].split(' ')[0] == "unsigned":
            unsigned = " " + decl['prototype'].split(' ')[1]
        else:
            unsigned = ""
        if decl['kind'] == "CXX_METHOD":
            if decl['is_virtual_method'] == True:
                virtual = "virtual "
            else:
                virtual = ""
            if decl['is_const_method'] == True:
                const = " const"
            else:
                const = ""
            if decl['access_type'] == "":
                allFunctions.append(decl['prototype'].split(' ')[0] + unsigned + " " + decl['displayname'] + const)
            elif decl['access_type'] == 'private':
                allPrivFunctions.append(virtual + decl['prototype'].split(' ')[0] + unsigned + " " + decl['parent_class'].split(' ')[1] + "::" + decl['displayname'] + const)
            elif decl['access_type'] == 'public':
                allPublicFunctions.append(virtual + decl['prototype'].split(' ')[0] + unsigned + " " + decl['parent_class'].split(' ')[1] + "::" + decl['displayname'] + const)
            elif decl['access_type'] == 'protected':
                allProtectedFunctions.append(virtual + decl['prototype'].split(' ')[0] + unsigned + " " + decl['parent_class'].split(' ')[1] + "::" + decl['displayname'] + const )
        elif decl['kind'] == "FUNCTION_DECL":
            if len(decl['prototype'].split('(')[0].split('**')) == 1 and len(decl['prototype'].split('(')[0].split('*')) == 1:
                allFunctions.append(decl['prototype'].split(' ')[0] + unsigned + " " + decl['displayname'] + const)
            elif len(decl['prototype'].split('**')) > 1:
                allFunctions.append(decl['prototype'].split('**')[0] + unsigned + "** " + decl['displayname'] + const)
            else:
                allFunctions.append(decl['prototype'].split(' ')[0] + unsigned + " * " + decl['displayname' + const])
        if decl['kind'] == "CLASS_DECL":
            allClasses.append("class " + decl['prototype'])
    
    #Write the YAML file
    file_yaml = {'classes': {'restriction': f'{restriction}', 'scope': 'global', 'names': list(set(allClasses))}, 'functions': {'restriction': f'{restriction}', 'scope': 'global', 'names': list(set(allFunctions))}, 'public_functions': {'restriction': f'{restriction}', 'scope': 'global', 'names': list(set(allPublicFunctions))}, 'private_functions': {'restriction': f'{restriction}', 'scope': 'global', 'names': list(set(allPrivFunctions))}, 'protected_functions': {'restriction': f'{restriction}', 'scope': 'global', 'names': list(set(allProtectedFunctions))}}
    with open("checkAPI.yaml", 'w') as file:
        yaml.dump(file_yaml, file)
    
    restrict(source, "checkAPI.YAML", output, hide)

    if not hide:
        checkAPI(compare, restriction, source, output, True)



if __name__ == "__main__":
    app()
