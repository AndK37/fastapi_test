from .base_models import *
from typing import List


class FilmSchema(BaseFilm):
    genres: List[BaseGenre]