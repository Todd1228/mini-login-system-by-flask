from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app import db
from app.models import User
from app.auth import login_required, admin_required
import cv2
import numpy as np
import base64

# 创建蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='')
user_bp = Blueprint('user', __name__, url_prefix='/user')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# YOLO 模型延迟加载
model = None

def get_model():
    """获取YOLO模型（延迟加载）"""
    global model
    if model is None:
        try:
            from ultralytics import YOLO
            print("正在初始化YOLO模型...")
            model = YOLO('yolov8n.pt')
            print("YOLO模型加载成功！")
        except Exception as e:
            print(f"YOLO模型加载失败: {e}")
            return None
    return model

# ============ AI 检测路由 ============

@user_bp.route('/detection')
@login_required
def detection():
    """AI 目标检测页面"""
    return render_template('user_detection.html')

@user_bp.route('/process_frame', methods=['POST'])
@login_required
def process_frame():
    """处理前端传来的摄像头帧"""
    data = request.json
    if not data or 'image' not in data:
        return jsonify({'error': 'No image data'}), 400
    
    # 获取YOLO模型
    yolo_model = get_model()
    if yolo_model is None:
        return jsonify({'error': 'YOLO model not initialized'}), 500
    
    # 解码 base64 图片
    try:
        img_data = data['image'].split(',')[1]
        img_bytes = base64.b64decode(img_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'error': 'Failed to decode image'}), 400
        
        # YOLO 检测
        results = yolo_model(img, conf=0.5, verbose=False)
        
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # 获取坐标 (x1, y1, x2, y2)
                b = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                label = yolo_model.names[cls]
                
                detections.append({
                    'bbox': [int(x) for x in b],
                    'label': label,
                    'confidence': round(conf, 2)
                })
        
        return jsonify({'detections': detections})
    except Exception as e:
        print(f"AI Detection Error: {e}")
        return jsonify({'error': str(e)}), 500

# ============ 认证路由（auth_bp）============

@auth_bp.route('/')
def index():
    """首页 - 根据登录状态重定向"""
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user and user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.profile'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('用户名和密码不能为空', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            if user.is_admin():
                flash(f'欢迎，{user.username}！', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash(f'欢迎，{user.username}！', 'success')
                return redirect(url_for('user.profile'))
        else:
            flash('用户名或密码错误', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """登出"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'{username} 已登出', 'info')
    return redirect(url_for('auth.login'))

# ============ 用户路由（user_bp）============

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """用户个人中心"""
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        old_password = request.form.get('old_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not old_password or not new_password or not confirm_password:
            flash('所有字段不能为空', 'danger')
        elif not user.check_password(old_password):
            flash('旧密码错误', 'danger')
        elif new_password != confirm_password:
            flash('两次输入的新密码不一致', 'danger')
        elif len(new_password) < 6:
            flash('密码长度至少6位', 'danger')
        else:
            user.set_password(new_password)
            db.session.commit()
            flash('密码修改成功', 'success')
    
    return render_template('user_profile.html', user=user)

# ============ 管理员路由（admin_bp）============

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """管理员首页 - 统计数据"""
    user_count = User.query.filter_by(role='user').count()
    admin_count = User.query.filter_by(role='admin').count()
    total_count = User.query.count()
    
    return render_template('admin_dashboard.html', 
                         user_count=user_count,
                         admin_count=admin_count,
                         total_count=total_count)

@admin_bp.route('/users')
@admin_required
def users():
    """用户管理页面"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = User.query.paginate(page=page, per_page=per_page)
    users_list = pagination.items
    
    return render_template('admin_users.html', 
                         users=users_list,
                         pagination=pagination)

@admin_bp.route('/users/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    """添加用户"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'user')
        
        if not username or not email or not password:
            flash('所有字段均不能为空', 'danger')
            return redirect(url_for('admin.add_user'))
        
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'danger')
            return redirect(url_for('admin.add_user'))
        
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash(f'用户 {username} 添加成功', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin_add_user.html')

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """编辑用户"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.email = request.form.get('email', '').strip()
        user.role = request.form.get('role', 'user')
        
        new_password = request.form.get('new_password', '').strip()
        if new_password:
            if len(new_password) < 6:
                flash('密码长度至少6位', 'danger')
                return redirect(url_for('admin.edit_user', user_id=user_id))
            user.set_password(new_password)
        
        db.session.commit()
        flash(f'用户 {user.username} 更新成功', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin_edit_user.html', user=user)

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """删除用户"""
    user = User.query.get_or_404(user_id)
    username = user.username
    
    db.session.delete(user)
    db.session.commit()
    flash(f'用户 {username} 已删除', 'success')
    return redirect(url_for('admin.users'))
