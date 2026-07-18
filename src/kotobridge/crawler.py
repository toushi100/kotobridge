#this class is responsible for crawling the folder and getting all the video and audio files in it and in subfolders and logs them to the console
import os
class Crawler:
    def __init__(self, folder_path, db):
        self.folder_path = folder_path
        self.files = []
        self.db = db

    def crawl(self):
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.mp3', '.wav', '.aac')):
                    if not self.__exists_in_db(self.db, file_path):
                        self.files.append(file_path)
                        print(f"Found file: {file_path}")
        
        return self

    def get_count(self):
        return len(self.files)
    
    def store_discovered_files(self):
        for file_path in self.files:
            self.db.insert(f"INSERT INTO videos (file_path, status) VALUES ('{file_path}', 0)")

    def __exists_in_db(self, db, file_path):
        existing_files = db.query(f"SELECT file_path FROM videos WHERE file_path = '{file_path}'")
        if existing_files:
            print(f"File already exists in database: {file_path}")
            return True
        return False
