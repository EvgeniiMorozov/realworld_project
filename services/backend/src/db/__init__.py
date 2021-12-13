from .connection import async_session, engine, get_db
from .models import *


users = User()
articles = Article()
comments = Comment()
tags = Tag()
followers = Follow()
favorites = Favorite()
