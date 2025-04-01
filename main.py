from fastapi import FastAPI, Query, Path, HTTPException
from models import *
from typing import List

db = [{
    'id': 1,
    'name': 'Товар',
    'price': 19.99,
    'desc': 'aaaaaaaa'
},
{
    'id': 2,
    'name': 'Товар',
    'price': 29.99,
    'desc': 'aaaaaaaa'
},
{
    'id': 3,
    'name': 'Товар',
    'price': 39.99,
    'desc': 'aaaaaaaa'
},
{
    'id': 4,
    'name': 'Товар',
    'price': 49.99,
    'desc': 'aaaaaaaa'
},
{
    'id': 5,
    'name': 'Товар',
    'price': 59.99,
    'desc': 'aaaaaaaa'
}]


app = FastAPI()

@app.get('/items', response_model=List[ItemGET])
def get_items(name: str | None = Query(default=None, min_length=2, example='Телефон'), 
              min_price: float | None = Query(default=None, gt=0, example=9.99), 
              max_price: float | None = Query(default=None, gt=0, example=99.99), 
              limit: int = Query(default=10, lt=101, gt=0, example=10)):

    if name == None:
        name = ''
    if min_price == None:
        min_price = 0
    if max_price == None:
        max_price = 0
        for i in db:    
            if i['price'] > max_price:
                max_price = i['price']

    if max_price < min_price:
        raise HTTPException(400,'Цена')
    
    a = []
    for i in db:
        if name in i["name"] and i["price"] >= min_price and i["price"] <= max_price:
            a.append(i)

    if len(a) == 0:
        raise HTTPException(404, 'Товар не найден')
    
    return a[:limit]

@app.get('/items/{item_id}', response_model=ItemGET)
def get_item_by_id(item_id:int = Path(gt=0, example=1)):
    for i in db:
        if i['id'] == item_id:
            return i
        
    raise HTTPException(404, 'Товар не найден')
        
@app.post('/items', response_model=ItemGET)
def create_item(item: ItemPOST):
    id = db[-1]['id'] + 1
    i = {'id': id, 'name': item.name, 'price': item.price, 'desc': item.desc}
    db.append(i)
    return i