from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    laptop = db.Column(db.String(255), index = True, unique = True)
    price = db.Column(db.String(255), index = True, unique = True)
    image = db.Column(db.String(255), index = True, unique = True)

    def __repr__(self):
        return '<User %r>' % (self.laptop)

