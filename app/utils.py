from flask import flash

def flash_message(message, category='info'):
    """显示闪现消息"""
    flash(message, category)

def get_current_user():
    """获取当前登录的用户"""
    from flask import session
    from app.models import User
    
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None
