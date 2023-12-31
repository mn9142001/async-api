import os
from pathlib import Path
from random import choices
from string import ascii_letters

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class File:
    
    def __init__(self, headers : dict, content : bytes) -> None:
        self.headers = headers
        self.content = content

    def generate_path(self):
        path = os.path.join(self.media_folder_path, self.file_name)
        if os.path.exists(path):
            random_name = "".join(choices(ascii_letters, k=7))
            path = os.path.join(
                self.media_folder_path, 
                f"{random_name}-{self.file_name}"
            )
            return path
        return path


    def make_file(self):
        self._path = self.generate_path()
        f = open(self._path, 'wb+')
        f.write(self.content)
        f.close()
            
    @property
    def media_folder_path(self):
        path = os.path.join(BASE_DIR, 'media')
        if not os.path.exists(path):
            os.makedirs(path)
        return path
            
    @property
    def path(self):
        if hasattr(self, '_path'):
            return self._path
        self.make_file()
        return self._path
    
    @property
    def file_name(self):
        if hasattr(self, '_file_name'):
            return self._file_name

        content_disposition : str = self.headers.get(b'Content-Disposition', b'').decode('utf-8')
        self._file_name = content_disposition.split('filename="')[1].split('"')[0]

        return self._file_name
    
    @property
    def name(self):
        if hasattr(self, '_name'):
            return self._name
        
        content_disposition = self.headers.get(b'Content-Disposition', b'').decode('utf-8')
        self._name = content_disposition.split('name="')[1].split('"')[0]
        return self._name