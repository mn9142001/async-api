import json
from exception import Http400

class SendResponseMixin:
    async def get_scope(self):
        return {
            'type': 'http.response.start',
            'status': self.status,
            'headers': self.get_headers(),
        }
        
    async def _send(self, *args, **kwargs):
        return await self.request.sender(*args, **kwargs)
        
    async def send(self, *args, **kwargs):
        scope = await self.get_scope()
        await self._send(
            scope
        )
        return await self._send(*args, **kwargs)
    

class RequestBodyDecoder:
    
    async def json_decoder(self, data):
        try:
            self._body = json.loads(data)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            error = f"Error parsing JSON: {str(e)}"
            raise Http400(error)
    
    async def get_raw_body(self):
        request_body = await self.rec()
        data = request_body.get('body', b'')
        return data        
    
    async def parse_body(self):
        data = await self.get_raw_body()
        
        if self.headers.is_json:
            return await self.json_decoder(data)
        
        raise Http400("API accepts only json")
            
    @property
    async def body(self):
        if self.method in ['GET', 'DELETE', 'OPTIONS']:  return
        
        if not hasattr(self, '_body'):
            await self.parse_body()
        
        return self._body
    