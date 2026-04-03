import typer
from kotobridge.translate import Translate
import time
app = typer.Typer()

@app.command()
def translate(name: str ):
    start_time = time.time()    
    if name is None:
        typer.echo("Please enter a valid text to translate")
        return None
    translate = Translate(name)
    result = translate.translate()

    end_time = time.time()
    typer.echo(f"Time taken: {end_time - start_time} seconds")
    return None

@app.command()
def main():
    # should get back to this later so the cli would be interactive
    typer.echo("!----------------------------------------------------------------! ")
    return None
    typer.echo("Welcome to Kotobridge!")
    typer.echo("Select an option:")
    typer.echo("1. Hello")
    typer.echo("2. Goodbye")
    typer.echo("3. Exit")
    choice = typer.prompt("Enter your choice:")

if __name__ == "__main__":
    app()