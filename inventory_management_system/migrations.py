from . import database
from . import models

def init_db():
    models.Base.metadata.create_all(bind=database.engine)
    #TODO: cleanup