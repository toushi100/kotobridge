import typer
from kotobridge.translate import Translate
import time
from kotobridge.crawler import Crawler

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
def crawl(folder_path: str):
    if folder_path is None:
        typer.echo("Please enter a valid folder path")
        return None
    crawler = Crawler(folder_path)
    crawler.crawl()
    print(f"Total files found: {crawler.get_count()}")
    return None
@app.command()
def main():
    # should get back to this later so the cli would be interactive
    typer.echo("!----------------------------------------------------------------! ")
    #'/Users/ahmed/Movies/クレヨンしんちゃん/クレヨンしんちゃん/1992/＃1-1　おつかいに行くゾ [1992-04-13][D2485D01].mp4'
    #'/home/ahmed/Developer/1992/＃1-1　おつかいに行くゾ [1992-04-13][D2485D01].mp4'
    return None
    typer.echo("Welcome to Kotobridge!")
    typer.echo("Select an option:")
    typer.echo("1. Hello")
    typer.echo("2. Goodbye")
    typer.echo("3. Exit")
    choice = typer.prompt("Enter your choice:")

if __name__ == "__main__":
    app()