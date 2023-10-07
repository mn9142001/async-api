
class SendResponseMixin:
    async def get_scope(self):
        return {
            'type': 'http.response.start',
            'status': self.status,
            'headers': self.get_headers(),
        }
        
    async def _send(self, *args, **kwargs):
        return await self.request.send(*args, **kwargs)
        
    async def send(self, *args, **kwargs):
        scope = await self.get_scope()
        await self._send(
            scope
        )
        return await self._send(*args, **kwargs)
    
