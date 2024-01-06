from config import db


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    elf_id = db.Column(db.Integer)
    title = db.Column(db.String(100))
    receiver = db.Column(db.String(100))
    delivery_date = db.Column(db.DateTime)
    delivered = db.Column(db.Boolean)
    create_date = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean)


class Elf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    assigned = db.Column(db.Integer)
    hire_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean)


class Holiday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    elf_id = db.Column(db.Integer)
    type = db.Column(db.String(50))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    create_date = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean)
