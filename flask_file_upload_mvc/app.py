import os
import logging
from flask import Flask
from extensions import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

os.makedirs(app.config['LOG_FOLDER'], exist_ok=True)
logging.basicConfig(
    filename=f"{app.config['LOG_FOLDER']}/app.log",
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

from controllers.file_controller import file_bp
from controllers.auth_controller import auth_bp

app.register_blueprint(file_bp)
app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)