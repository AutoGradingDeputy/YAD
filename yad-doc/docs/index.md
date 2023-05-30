# Welcome to YAD


## What is YAD?
YAD is a set of CLI tools that streamlines the process of building an automatic grader for C++ programming assignments. It provides a set of features that instructors and developers can incorporate into their existing automatic graders to save time and improve the grading process. 

## Who benifits from YAD? 
The target audience of YAD includes instructors and developers in any programming field who are looking for ways to make the grading process more efficient and effective.

## Getting Started

* To install YAD, run the following command
* `pip install Y4D`

## Updating YAD

* To update YAD, run the following command
* `pip install --upgrade Y4D`

## Deleting YAD

* To delete YAD, run the following command
* `pip uninstall Y4D`

## YAD tools
### [Isolator](./yad-doc/docs/isolator.md)
Isolates a function or list of functions or classes inside the code and replace them with their counterparts from the reference code.
### [Restrictor](./yad-doc/docs/restrictor.md)
Restricts the use of certain functions, libraries, and keywords inside the code.
### [CheckAPI](./yad-doc/docs/checkAPI.md)
Checks if signature of all functions in the code follows all signatures in a given code.
### [Comment Controller](./yad-doc/docs/commentController.md)
Extracts and deletes comments, comments out a given function or clas in the code.

## Supported Language 
<div class="bs-callout bs-callout-warning">
  <h4>Warning</h4>
  YAD supports C++ with versions older than C++ 11.0
</div>

## Windows Users Issues
In some cases YAD will be installed in a path that is not in your enivronment variables, in order to solve that do the following:

* Copy the path of YAD provided by pip install command in CMD.
* Press windows and break button, or go to settings then about.
* Choose Advanced system settings.
* Choose Environment Varibales.
* Press on the Path then press Edit...
* Press New then paste the path you copied in the first step.
* Press ok then ok.
* YAD should be ready to use in your windows CMD.
