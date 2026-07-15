#this class is responsible for crawling the folder and getting all the video and audio files in it and in subfolders and logs them to the console
import os
class Crawler:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.files = []

    def crawl(self):
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.mp3', '.wav', '.aac')):
                    self.files.append(file_path)
                    print(f"Found file: {file_path}")
        return self

    def get_count(self):
        return len(self.files)
    
    def store_discovered_files(self, db):
        for file_path in self.files:
            db.insert(f"INSERT INTO videos (file_path, status) VALUES ('{file_path}', 0)")