from pydantic import BaseModel


class BaseModel(BaseModel):
    
    async def validate_data(data : dict):
        return data
    

BaseModel.model_config["from_attributes"]=True