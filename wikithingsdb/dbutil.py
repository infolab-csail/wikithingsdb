from models import db

def insert_batch(model, batch):
    db.connect()
    with db.atomic():
        model.insert_many(batch).execute()
    db.close()
