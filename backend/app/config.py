import os


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    TESTING = False
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True
    # A separate database so tests never touch development data.
    # Falls back to in-memory SQLite so `pytest` works without Docker.
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL", "sqlite://")
    SECRET_KEY = "test-only-key"
    JWT_SECRET_KEY = "test-only-jwt-key-that-is-long-enough-for-hs256"

    BOOKING_HOLD_MINUTES = 15
    CANCEL_CUTOFF_HOURS = 2

    # Off, as in production; bus tests switch it on with the `bus` fixture.
    FEATURE_BUS_BOOKING = False
    UPLOAD_DIR = None  # each test that uploads sets its own temporary folder

    # Tests never talk to the real MoMo or SMS services.
    MOMO_SUBSCRIPTION_KEY = MOMO_API_USER = MOMO_API_KEY = MOMO_CALLBACK_URL = None
    MOMO_TARGET_ENVIRONMENT = "sandbox"
    MOMO_CURRENCY = "EUR"
    AT_USERNAME = AT_API_KEY = None


class ProductionConfig(BaseConfig):
    pass


CONFIGS = {
    "development": DevelopmentConfig,
    "testing": TestConfig,
    "production": ProductionConfig,
}
