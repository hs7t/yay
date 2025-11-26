import typer
from tokenization import Tokenizer
from parsing import Parser
from running import runInstructions

from rich import print
from pathlib import Path

app = typer.Typer(add_completion = False)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    print("[bold yellow]🤸 yay trampoline v0.1[/bold yellow]")
    print("/ try --help!")

@app.command()
def run(
    file: str = typer.Argument("A .yay file to run")
):
    workingFile = Path(file).resolve()
    if not workingFile.exists():
        print("/ hmm. it seems that file doesn't exist.")
        raise typer.Exit(code=1)
    if not workingFile.is_file():
        print("/ hold on! are you sure that's a file?")
        raise typer.Exit(code=1)
    if not workingFile.suffix == ".yay":
        print("/ aah! that doesn't seem to be a valid yay script file.")
        if workingFile.suffix == ".xml":
            print("/ ...XML??? ew???")
        raise typer.Exit(code=1)
    
    yayfile = open(file, "tr")
    yaytext = yayfile.read()

    tokens = Tokenizer(yaytext).getTokens()
    instructions = Parser(tokens).getInstructions()

    print("[blue]/ reading instructions...[/blue]")
    runInstructions(instructions)

if __name__ == "__main__":
    app()