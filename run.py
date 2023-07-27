from app import app, database
from app.models.tables_db import CardProject

with app.app_context():
    database.create_all()
    database.session.commit()

if __name__ == "__main__":

    app.run()
