from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    paid_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    paid_by_user = db.relationship('User', backref=db.backref('expenses', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'description': self.description,
            'paid_by_user_id': self.paid_by_user_id
        }

class Split(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    expense = db.relationship('Expense', backref=db.backref('splits', lazy=True))
    user = db.relationship('User', backref=db.backref('splits', lazy=True))