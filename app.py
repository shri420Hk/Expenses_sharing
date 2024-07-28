from flask import Flask
from database import db  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  

if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()
    
    # Import routes after creating database
    from routes import init_routes
    init_routes(app)
    app.run(debug=True)