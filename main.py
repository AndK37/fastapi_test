from fastapi import FastAPI, Query
from random import randint

app = FastAPI()

@app.get('/')
def read_root():
    return {'hello': 'world', 'goodbye': 'world'}

@app.get('/about_me')
def read_about_me():
    return {
        'name': 'Andrey',
        'age': 20,
        'alive': True
    }

@app.get('/rnd')
def get_random_int():
    return randint(1, 10)
@app.get('/triangle')
def get_triangle_square(a:int = Query(gt=0), b:int = Query(gt=0), c:int = Query(gt=0)):
    if a > b + c:
        return {'err': 'not exist'}
    if b > a + c:
        return {'err': 'not exist'}
    if c > b + a:
        return {'err': 'not exist'}
    
    p = (a + b + c) / 2
    S = (p * (p - a) * (p - b) * (p - c))**0.5

    return {'a': a, 'b': b, 'c': c, 'p': p, 'S': S}


