from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate
from routes.transactions import transactions_bp
from routes.summary import summary_bp
from routes.ranking import ranking_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    app.register_blueprint(transactions_bp)
    app.register_blueprint(summary_bp)
    app.register_blueprint(ranking_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)