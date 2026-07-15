import os

import typer
from kotobridge.translate import Translate
import time
from kotobridge.crawler import Crawler
from db.init_db import DB

STATUS_MAP = {
    "discovered": 0,
    "in_progress": 1,
    "transcribed": 2,
    "translated": 3
}

app = typer.Typer()




@app.command()
def translate(path: str ):
    if is_folder(path):
        crawl(path)
    else:
        start_time = time.time()    
        if path is None:
            typer.echo("Please enter a valid file path to translate")
            return None
        translate = Translate(path)
        result = translate.translate()

        end_time = time.time()
        typer.echo(f"Time taken: {end_time - start_time} seconds")
        return None


@app.command()
def crawl(folder_path: str):
    db = DB()
    db.connect()
    
    if folder_path is None:
        typer.echo("Please enter a valid folder path")
        return None
    crawler = Crawler(folder_path)
    crawler.crawl()
    print(f"Total files found: {crawler.get_count()}")
    crawler.store_discovered_files(db)
    videos_count = db.query("SELECT * FROM videos")
    print(f"Total files stored in database: {len(videos_count)}") 
    return None

@app.command()
def clear_db():
    db = DB()
    db.clear_db()
    print("Database cleared")
    return None

def is_folder(path: str):
    return os.path.isdir(path)

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