import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class File:
    
    def __init__(self, headers : dict, content : bytes) -> None:
        self.headers = headers
        self.content = content
        
    async def make_file(self):
        self._path = os.path.join(await self.media_folder_path, await self.file_name)
        f = open(self._path, 'wb')
        f.write(self.content)
    
    @property
    async def media_folder_path(self):
        path = os.path.join(BASE_DIR, 'media')
        if not os.path.exists(path):
            os.makedirs(path)
        return path
            
    @property
    async def path(self):
        if hasattr(self, '_path'):
            return self._path
        await self.make_file()
        return self._path
    
    @property
    async def file_name(self):
        if hasattr(self, '_file_name'):
            return self._file_name

        content_disposition : str = self.headers.get(b'Content-Disposition', b'').decode('utf-8')
        self._file_name = content_disposition.split('filename="')[1].split('"')[0]

        return self._file_name
    
    @property
    async def name(self):
        if hasattr(self, '_name'):
            return self._name
        
        content_disposition = self.headers.get(b'Content-Disposition', b'').decode('utf-8')
        self._name = content_disposition.split('name="')[1].split('"')[0]
        return self._name