import os
from datetime import timedelta

class Config:
    """基础配置"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-me')
    
    # 使用SQLite数据库（无需MySQL配置）
    DATABASE_URL = "sqlite:///flask_login.db"
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session配置
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # 开发环境设为False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_NAME = 'flask_login_session'


class DevelopmentConfig(Config):
    """开发配置"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """生产配置"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True

config = DevelopmentConfig if os.getenv('FLASK_ENV') == 'development' else ProductionConfig
