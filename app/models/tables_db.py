from app import database


class CardProject(database.Model):
    __tablename__ = "cards"

    id = database.Column(database.Integer, primary_key=True)
    image_url = database.Column(database.String, nullable=True)
    title = database.Column(database.String, nullable=True, unique=True)
    description = database.Column(database.String, nullable=True)
    demo_url = database.Column(database.String, nullable=True)
    git_code_url = database.Column(database.String, nullable=True)
    like_count = database.Column(database.Integer, default=0)

    #  Under we have the constructor, when the card is created
    def __init__(self, image_url, title, description, demo_url, git_code_url, like_count):
        self.image_url = image_url
        self.title = title
        self.description = description
        self.demo_url = demo_url
        self.git_code_url = git_code_url
        self.like_count = like_count

    # Under we have the function show how will see when search em db
    def __repr__(self):
        return "<CardProject %r>" % self.title


class Tasks(database.Model):
    __tablename__ = "tasks"
    id = database.Column(database.Integer, primary_key=True)
    content = database.Column(database.String(200), nullable=True)
    done = database.Column(database.Boolean)