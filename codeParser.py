import json
import clang.cindex
import re
from pathlib import Path

def findLocationFunction(data, prototype: str, source):
    #Check for static, virtual, pure virtual, and constructors
    is_static = False
    is_pure = False
    is_virtual = False
    has_initializer = "false"
    
    #Check constructors with initializer lists
    if len(prototype.split("(")) > 2:
        has_initializer = "true" 

    #Check static functions
    if len(prototype.split("static")) > 1:
        is_static= True

    #Check virtual and pure virtual functions
    if len(prototype.split("virtual")) > 1:
        is_virtual= True
        if len( prototype.split("=0")) > 1:
            prototype = prototype.split("=0")[0]
            is_pure= True
        elif len( prototype.split("= 0")) > 1:
            prototype = prototype.split("= 0")[0]
            is_pure= True
            
    #Label function by its type 
    if len(prototype.split("template"))> 1 :
        if len(prototype.split("::")) > 1 :
            type = "template_member_function"
        else:
            type = "template_function"
    elif len(prototype.split("::")) > 1:
        type = "member_function"
    else:
        type="function"
    
    #Extract information from function prototype
    if type == "member_function" or type == "template_member_function":
        parent_class = prototype.split("::")[0].strip().split(" ")[-1]
        returntype = prototype.split(parent_class)[0].strip().split(" ")[-1]
        prototype=prototype.replace(" ", "")
        name = prototype.split("::")[1].split("(")[0]
        if len(name.split("~")) > 1 and name.split("~")[1] == parent_class:
            type = "decstructor"
        if name == parent_class:
            type = "constructor"   
    else:
        if type == "template_function":
            prototype = prototype.split(">")[1].strip()
        name = prototype.split('(')[0].split(" ")[-1].strip()
        returntype = prototype.split(name)[0].strip()
        
    if type == "constructor" or type == "decstructor":
        returntype = "void"
        params = "(" + prototype.split("::")[1].split("(")[1]
        if has_initializer == "true": 
            params = params.split(":")[0]
    else:
        params = prototype.split(name)[1]
        
    qualtype = returntype + params
    qualtype = qualtype.replace(" ", "")

    #Retrieve position of function
    pos=[]
    if type == "function":
        for item in data['nodes']:
            if item['kind'] == "FUNCTION_DECL" and item['spelling'].replace(" ", "") == name and item['prototype'].replace(" ", "") == qualtype:
                if is_static == item['is_static_method'] and is_virtual == item['is_virtual_method'] and is_pure == item['is_pure']:
                    end = item['end']
                    start = item['start']
                    pos += [start, end, type, item['access_type']]
    if type == "member_function":
        for item in data['nodes']:
            if item['kind'] == "CXX_METHOD" and item['spelling'].replace(" ", "") == name and item['prototype'].replace(" ", "") == qualtype and item['parent_class']!="" and parent_class == item['parent_class'].split(" ")[1]:
                if is_static == item['is_static_method'] and is_virtual == item['is_virtual_method'] and is_pure == item['is_pure']:
                    end = item['end']
                    start = item['start']
                    pos += [start, end, type, item['access_type']]          
    if type == "template_function" or type == "template_member_function":
        for item in data['nodes']:
            if (item['kind'] == "FUNCTION_TEMPLATE" and item['spelling'].replace(" ", "") == name and item['prototype'].replace(" ", "") == qualtype and is_static == item['is_static_method'] and ((type == "template_function" and item['access_type'] == "invalid") or ( type == "template_member_function" and item['parent_class'] != "" and parent_class == item['parent_class'].split(" ")[1])  )  ):
                    start = item['start']
                    end =-1
                    with open(source, "r") as source_file:
                        lines = source_file.readlines()    
                    #Check for forward declaration 
                    openb =0
                    for char in lines[start-1]:
                        if char == '{':
                            openb = openb+1
                    if openb == 0:
                        pos += [start, start, type, item['access_type']]
                        continue
                    #Find where the function ends 
                    i = start 
                    while(True):
                        for char in lines[i]:
                            if char == '{':
                                openb = openb+1
                            if char == '}':
                                openb = openb -1
                                if openb == 0:
                                    end = i+1
                                    break
                        i = i+1
                        if end != -1:
                            break
                    pos += [start, end, type, item['access_type']] 
    if type == "constructor":
        for item in data['nodes']:
            if item['kind'] == "CONSTRUCTOR" and item['spelling'].replace(" ", "") == name and item['prototype'].replace(" ", "") == qualtype and item['initializer_list'] == has_initializer:
                end = item['end']
                start = item['start']
                pos += [start, end, type, item['access_type']] 
    if type == "decstructor":
        for item in data['nodes']:
            if item['kind'] == "DESTRUCTOR" and item['spelling'].replace(" ", "") == name:
                end = item['end']
                start = item['start']
                pos += [start, end, type, item['access_type']] 
        
    return pos

def findLocationClass(data, prototype: str, source, type: str, iteration = 0):
    #classes list stores all classes that inherits from\friend with main class in order to parse their member functions and nested classes  
    classes =  [prototype]
    pos=[]
    for class_i in classes:
        name = class_i.split(" ")[1]
        class_start = -1
        class_end = -1
        flag=0
        i=0 
        while i < len(data['nodes']):
            item = data['nodes'][i]
            #find start and end positions of a class given its name
            if item['spelling'] == name:
                if ((item['is_class'] == True and type == "class") or (item['is_struct'] == True and type == "struct")):
                    start = item['start']
                    end = item['end']
                    class_start = start 
                    class_end = end
                    pos+=[start, end, type, ""]
                    flag =1
                elif item['kind'] == "CLASS_TEMPLATE":
                    start = item['start']
                    # in-case the template definition was on the previous line
                    if item['col'] <= 12:
                        start -= 1
                    end = item['end']
                    class_start = start 
                    class_end = end
                    pos+=[start, end, type, ""]
                    flag =1
                
            if flag  == 0 : 
                i = i+1
                continue
            #check member functions implemented outside the class
            if item['start'] < class_start or item['end'] > class_end:
                if item['mangled_name'].startswith('?'):
                    mangledName= item['mangled_name'].split("@")
                    if len(mangledName) > 1 and mangledName[1] == name:
                        if item['kind'] == "CXX_METHOD":
                            returnType = item['prototype'].split(" ")[0]
                            func_prototype = returnType +" " + name + "::" +item['displayname']
                            pos+= findLocationFunction(data, func_prototype, source)
            #check template member functions  
            if item["kind"] == "FUNCTION_TEMPLATE":
                start_line = item['start']
                j = i+1
                template_node = data['nodes'][j]
                while  j < len(data['nodes']) and template_node['start'] == start_line:
                    if template_node['kind'] == "TEMPLATE_TYPE_PARAMETER":
                        template = template_node['spelling']
                    if template_node['kind'] == "TYPE_REF" and template_node['spelling'] == prototype:
                        returnType = item['prototype'].split(" ")[0]
                        func_prototype = "template <typename " + template + "> " + returnType +" " + name + " :: " +item['displayname']
                        pos += findLocationFunction(data, func_prototype, source)
                    template_node = data['nodes'][j]    
                    j+=1 
            #find start and end positions of all classes that inherits from this class       
            for inherit in item['inherits_from']:
                if inherit == name:
                    start = item['start']
                    end = item['end']
                    classes += [type + " "+  item['spelling']]            
            #find start and end positions of all classes with friendship with this class
            for friend in item['friend_with']:
                if friend == class_i:
                    start = item['start']
                    end = item['end']
                    classes +=  [type + " "+  item['spelling']]
            i = i+1
        if iteration == 1:
            return pos

    return pos
 


#find if a constructor has expression initializer list
def hasInitializerList(cursor):
    for child in cursor.get_children():
        if child.kind.is_expression():
            return True
    return False



#Compile code and return parse tree
def prepareData (source: str):
    
    #Get Code from source
    with open(source, 'r') as file:
        source = file.read()

    #String manipulate source for parse to work (removing libraries and using namespace)
    source = re.sub(r'^#include\s*[\s\S][<"]\S+[>"]$', r'// \g<0>', source, flags=re.MULTILINE)
    source = re.sub(r'^\s*using\s+namespace\s+\S+;$', r'// \g<0>', source, flags=re.MULTILINE)

    index = clang.cindex.Index.create()
    tu = index.parse('dud.cpp', unsaved_files=[('dud.cpp', source)])
    
    output = {"nodes": []}
    friendFlag = False
    classPointer = -1
    for node in tu.cursor.walk_preorder():
        access_type =""
        parent_class = ""
        initializer_list = "false"
        #Check if the constructor has an expression initializer list
        if node.kind == clang.cindex.CursorKind.CONSTRUCTOR:
            if hasInitializerList(node):
                initializer_list = "true"
                
        #Save access type of member functions, anything else will have value "invalid"              
        access_type = str(node.access_specifier).split(".")[1]
        #Save name of parent class
        if access_type == "INVALID":
            parent_class = ""
        else:
            parent = node.semantic_parent
            if parent is None:
                parent_class=""
            elif parent.kind == clang.cindex.CursorKind.CLASS_DECL:
                parent_class = "class " + str(parent.spelling)
            elif parent.kind == clang.cindex.CursorKind.STRUCT_DECL:
                parent_class = "struct " + str(parent.spelling)
            
        if node.kind == clang.cindex.CursorKind.CLASS_DECL:
            classPointer = 0
            friendFlag = False
            
        elif node.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
            inh = node.spelling
            output["nodes"][classPointer]["inherits_from"].append(inh)

        elif node.kind == clang.cindex.CursorKind.FRIEND_DECL:
            friendFlag = True

        elif friendFlag:
            friend = node.spelling
            if len(friend.split("class")) == 1: #check this: or len(friend.split("struct")):
                friend = node.type.spelling.split('(')[0] + node.displayname
            output["nodes"][classPointer]["friend_with"].append(friend)
            friendFlag = False

        classPointer = classPointer - 1

        #Backbone of the project, retuning parse tree information.
        node_dict = {
            "kind": str(node.kind.name),
            "spelling": node.spelling,
            "prototype": node.type.spelling,
            "displayname": node.displayname,
            "type": str(node.type),
            "start": int(node.location.line),
            "end": int(node.extent.end.line),
            "col": int(node.location.column),
            "mangled_name": node.mangled_name,
            "is_const_method": node.is_const_method(),
            "is_static_method": node.is_static_method(),
            "is_virtual_method": node.is_virtual_method(),
            "is_pure": node.is_pure_virtual_method(),
            "is_struct": node.kind == clang.cindex.CursorKind.STRUCT_DECL,
            "is_class": node.kind == clang.cindex.CursorKind.CLASS_DECL,
            "inherits_from": [],
            "friend_with": [],
            "access_type" : access_type.lower(),
            "parent_class" : parent_class,
            "initializer_list" : initializer_list,
        }
        output["nodes"].append(node_dict)
    
    jsonFormat = json.dumps(output, indent=4)
    data = json.loads(jsonFormat)

    return data


#Return postions of anything the user is searching for.
def positions ( source: str, type: str, prototype: str, option = 0):
    source_path = Path(source)
    if source_path.exists() == False:
        print("Error: " + source + " doesn't exist")
        return ["error"]
    
    #Checking if it is a .h file and converting it to .cpp, due to libclang requirements
    file_extension = source_path.suffix
    if file_extension == ".h":
        file_name = source_path.stem
        with open(source, 'r') as source:
            content = source.read()
        destination_file = file_name + ".cpp"
        with open(destination_file, 'w') as destination:
            destination.write(content)
        source = destination_file
        
    #Compiling the code
    data = prepareData(source)
    
    #Varibale for saving position of anything the user is searching for.
    pos =[]
    
    if type == "class" or type == "struct":
        pos = findLocationClass(data, prototype , source, type, option)  
        
    if type == "function":
        pos = findLocationFunction( data, prototype, source)  
        
    return pos
