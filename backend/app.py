from flask import Flask
from config import Config
from extensions import db, migrate, cors
from routes.flights import flights_bp
from routes.bookings import bookings_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Register isolated route modules
    app.register_blueprint(flights_bp)
    app.register_blueprint(bookings_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)