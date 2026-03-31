import typer

app = typer.Typer()

@app.command()
def hello(name: str = "world"):
    print(f"Hello, {name}!")

@app.command()
def goodbye(name: str = "world"):
    print(f"Goodbye, {name}!")

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