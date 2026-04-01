from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os

db = SQLAlchemy()

def create_app():
    """创建Flask应用"""
    # 获取项目根目录
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')
    
    # 创建Flask应用，显式指定templates和static路径
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    # 禁用Jinja2缓存，强制每次重新加载模板
    app.jinja_env.cache = None
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    
    # 加载配置
    from app.config import DevelopmentConfig
    app.config.from_object(DevelopmentConfig)
    
    # 初始化扩展
    db.init_app(app)
    Session(app)
    
    # 注册路由蓝图
    from app.routes import auth_bp, user_bp, admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app
