from functools import wraps
from flask import session, redirect, url_for, request

def login_required(f):
    """检查用户是否登录的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """检查用户是否为管理员的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login', next=request.url))
        
        from app.models import User
        user = User.query.get(session.get('user_id'))
        if not user or not user.is_admin():
            return redirect(url_for('user.profile'))
        
        return f(*args, **kwargs)
    return decorated_function
