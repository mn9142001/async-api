import json
from urllib.parse import parse_qs


class QueryParameter:
    
    def __init__(self, query : str) -> None:
        self.query = parse_qs(query)
            
    async def __str__(self) -> str:
        return json.dumps(self.query)
    
    def __getitem__(self, item):
         return self.query[item]
     
    
    async def getlist(self, name, default=None):
        try:                
            return self.query[name]
        except KeyError as e:
            return default
    
    