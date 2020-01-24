from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agenda_slug=db.Column(db.String(120),nullable=False)
    full_name= db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address =db.Column(db.String(120),unique=True,nullable=False)
    phone = db.Column(db.Integer,unique=True,nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "full_name":self.full_name,
            "email":self.email,
            "address":self.address,
            "phone":self.phone,
            "agenda_slug":self.agenda_slug,
             "id":self.id}