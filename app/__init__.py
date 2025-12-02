from flask import Flask
import redis
from .config import Config

r = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    decode_responses=True
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    return app
