
from models import init_db
from flask_cors import CORS
from flask import Flask
from routes.auth_routes import auth_bp
from routes.task_routes import task_bp



app = Flask(__name__)

CORS(app)  
app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)

init_db()
print("Database initialized successfully.")

if __name__ == "__main__":
    app.run(debug=True,port=8000)



