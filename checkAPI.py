import typer
import restrictor

app = typer.Typer()

#Function to restrict a single (private/public/protected) function, no need for the YAML file, further explanation available exactly below function definition.
@app.command("")
def main(source: str  = typer.Argument(..., help="The path of the .cpp or .h file the user wants restrictor to work on."),
        compare: str = typer.Argument(..., help="The path of the .cpp or .h file the user wants the source file to be compared to."),
        restriction: str = typer.Argument(..., help="The restriction type used for 2 ways of checking:\n\nat_least: Everything being checked must exist (It can be with other functions/classes).\n\nexactly: Everything being checked must only exist (It can not be with other functions/classes)."),
        output: str  = typer.Option("n", "-o", help="If n this will make checkAPI print the number of missing functions/classes then extra functions/classes, Input V if you want a list of violations to be printed and more information (default is n) (Takes only v or V or n or N)."),
        hide:bool = typer.Argument(False, hidden=True, help="A hidden variable for developers use, used to return extra functions and classes found in the code.")):
    """
    This tool will compare two files together, the source and compare file, it will check if the function prototypes and class names match then return true or false accordingly.
    """
    restrictor.checkAPI(source, restriction, compare, output, hide)


if __name__ == "__main__":
    app()
