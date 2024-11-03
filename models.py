from init import db 

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class BankDetail(db.Model):
    __tablename__ = 'bank_details'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    bic = db.Column(db.String(20), nullable=False)
    account_number = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
