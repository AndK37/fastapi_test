from pydantic import BaseModel, Field

class ItemPOST(BaseModel):
    name:str = Field(min_length=2, max_length=100, example='Телефон')
    price: float = Field(gt=0, example=9.99)
    desc: str | None = Field(default=None, max_length=500, example='Крутой телефон')

class ItemGET(BaseModel):
    id: int = Field(gt=0)
    name:str = Field(min_length=2, max_length=100, example='Телефон')
    price: float = Field(gt=0, example=9.99)
    desc: str | None = Field(default=None, max_length=500, example='Крутой телефон')

