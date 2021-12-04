from db.base import *
from db.models import *

metadata.create_all(bind=engine)
