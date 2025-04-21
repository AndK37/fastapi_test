from pydantic import BaseModel, Field
from typing import List



class CreateGenre(BaseModel):
    name: str = Field(example='фантастика', min_length=1, max_length=255)
    desc: str | None = Field(example='Направление и жанр художественной кинематографии, который можно охарактеризовать повышенным уровнем условности.', min_length=0, max_length=255, default=None)

class CreateFilm(BaseModel):
    name: str = Field(example='Интерстеллар', min_length=1, max_length=255)
    year: int = Field(example=2014, gt=0)
    duration: float = Field(example=169.0, gt=0.0)
    rating: float = Field(example=8.7, ge=0.0, le=10.0)
    desc: str | None = Field(example='Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями.', default=None)
    genres: List[int] | None = Field(default=[1])
