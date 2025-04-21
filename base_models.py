from pydantic import BaseModel, Field
from datetime import date



class BaseFilmShort(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example='Интерстеллар')

class BaseFilm(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example='Интерстеллар')
    year: int = Field(example=2014)
    duration: float = Field(example=169.0)
    rating: float = Field(example=8.7)
    desc: str | None = Field(example='Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями.', default=None)
    poster: str | None = Field(example='./img/1.png')
    add_date: date = Field(example=date(2025, 4, 19))

class BaseGenre(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example='фантастика')
    desc: str | None = Field(example='Направление и жанр художественной кинематографии, который можно охарактеризовать повышенным уровнем условности.')
