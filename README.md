# Flask登录系统 + AI目标检测 - 运行指南

## 📋 项目概览

这是一个完整的Flask Web应用，集成了用户和管理员双端登录功能，以及 YOLOv8 AI 实时目标检测，包含：
- ✅ 用户/管理员统一登录界面
- ✅ 用户个人中心（修改密码）
- ✅ 管理员后台（用户增删改查）
- ✅ Session会话管理
- ✅ Bcrypt密码加密
- ✅ SQLite数据库（无需外部配置）
- ✅ **【新增】YOLOv8 AI实时目标检测**
- ✅ **【新增】摄像头实时视频流分析**

---

## 🚀 快速开始

### 第1步：安装Python依赖

在项目根目录打开终端，运行：

```bash
pip install -r requirements.txt
```

或者使用 Tsinghua 镜像加速（国内推荐）：

```bash
pip install -i https://mirrors.tsinghua.edu.cn/pypi/web/simple -r requirements.txt
```

**主要依赖包括**：
- Flask（Web框架）
- Flask-SQLAlchemy（数据库ORM）
- Flask-Session（会话管理）
- bcrypt（密码加密）
- ultralytics（YOLOv8目标检测）
- opencv-python（图像处理）
- numpy（数值计算）

### 第2步：配置环境变量

编辑 `.env` 文件：

```ini
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
SECRET_KEY=your-secret-key-here
```

💡 **注意**：本项目使用 SQLite 数据库，无需额外配置 MySQL/PostgreSQL

### 第3步：初始化数据库

运行初始化脚本，创建表并插入测试数据：

```bash
python init_db.py
```

你会看到类似输出：

```
✓ 数据库初始化成功
✓ 默认管理员账号已创建
✓ 默认测试用户已创建
```

### 第4步：启动Flask应用

```bash
python run.py
```

你会看到：

```
🚀 Flask服务器启动
📍 访问地址: http://localhost:5000
🔑 登录账号:
   管理员: admin / admin123
   用户: user / user123
按 Ctrl+C 停止服务器
```

---

## 🌐 访问应用

打开浏览器，访问：**http://localhost:5000**

### 功能演示流程

#### 👤 普通用户流程：
1. 用户名：`user`，密码：`user123`
2. 登录后进入用户个人中心
3. 可修改密码
4. 点击 **🔍 AI 检测** 进入实时目标检测页面
   - 允许摄像头访问，即可看到实时图像
   - 自动检测画面中的物体（人、动物、物品等）
   - 显示物体名称和置信度
5. 点击"登出"退出登录

#### 👨‍💼 管理员流程：
1. 用户名：`admin`，密码：`admin123`
2. 登录后进入管理员后台
3. 查看统计数据（用户数、管理员数等）
4. 进入"用户管理"页面进行用户管理：
   - ➕ 添加新用户
   - ✏️ 编辑用户（邮箱、角色、密码）
   - 🗑️ 删除用户
5. 同样可以使用 **🔍 AI 检测** 功能进行目标检测
6. 点击"登出"退出登录

---

## 📁 项目结构

```
test/
├── app/
│   ├── __init__.py        # 应用工厂
│   ├── config.py          # 配置管理
│   ├── models.py          # 数据库模型（User）
│   ├── routes.py          # 所有路由（含AI检测路由）
│   ├── auth.py            # 认证装饰器
│   └── utils.py           # 工具函数
├── templates/             # HTML模板
│   ├── base.html          # 基础模板
│   ├── login.html         # 登录页面
│   ├── user_profile.html  # 用户中心
│   ├── user_detection.html    # 【新增】AI目标检测页面
│   ├── admin_dashboard.html   # 管理员首页
│   ├── admin_users.html       # 用户管理
│   ├── admin_add_user.html    # 添加用户
│   └── admin_edit_user.html   # 编辑用户
├── static/
│   ├── css/
│   │   └── style.css      # 全局样式（含检测页面样式）
│   └── js/
│       └── main.js        # JavaScript交互
├── yolov8n.pt             # 【新增】YOLOv8模型文件
├── flask_login.db         # SQLite数据库文件
├── requirements.txt       # Python依赖
├── .env                   # 环境配置
├── .gitignore            # Git忽略规则
├── run.py                # 启动脚本
├── init_db.py            # 数据库初始化脚本
└── README.md             # 本文件
```

---

## 🔑 测试账户

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 普通用户 | user | user123 |
| 测试用户 | testuser2-5 | password123 |

**💡 提示**：在登录页面点击账户卡片可快速填充用户名和密码！

---

## 🔐 主要功能说明

### 认证系统
- 使用Bcrypt加密密码，提高安全性
- 基于Flask-Session的会话管理
- 装饰器 `@login_required` 保护用户页面
- 装饰器 `@admin_required` 保护管理员页面

### 用户管理
- 用户可以修改自己的密码
- 管理员可以创建、编辑、删除用户
- 支持给用户分配"普通用户"或"管理员"角色

### 数据库
- 使用SQLite数据库（自轻便，无需额外配置）
- SQLAlchemy ORM进行数据库操作
- 自动时间戳（created_at, updated_at）

### 🤖 AI目标检测（NEW）
- **YOLOv8实时检测**：使用YOLOv8-nano模型进行高效目标检测
- **摄像头支持**：直接访问用户摄像头进行实时分析
- **即插即用**：无需手动配置，模型自动下载
- **支持的物体**：人、动物、车辆、日用品等肢80多种类别
- **实时反馈**：显示检测到的物体名称和置信度
- **跨浏览器**：支持所有现代浏览器（Chrome、Firefox、Edge等）
- **路由**：
  - `GET /user/detection` - 检测页面
  - `POST /user/process_frame` - 图像处理API

---

## 🐛 常见问题

### Q: 摄像头无法访问
**A**: 检查以下几点：
1. 浏览器是否允许访问摄像头（第一次访问会提示）
2. 操作系统权限设置中，浏览器是否有摄像头权限
3. 摄像头是否被其他应用占用
4. 汣试在隐私浏览模式下访问

### Q: AI检测很慢
**A**: 这是正常的，原因：
1. YOLOv8第一次运行需要加载模型（约50MB）
2. GPU不可用时使用CPU进行计算较慢
3. 高分辨率输入会增加处理时间

**优化方案**：
- 降低摄像头分辨率
- 如果有GPU，确保已安装CUDA和torch GPU版本

### Q: 模型文件愿化
**A**: 删除 `yolov8n.pt` 文件，下次访问检测页面会自动重新下载

### Q: `ModuleNotFoundError: No module named 'xxx'`
**A**: 重新安装依赖：
```bash
pip install -r requirements.txt
```

### Q: 忘记了管理员密码
**A**: 删除数据库并重新初始化：
```bash
# 在MySQL中执行
DROP DATABASE flask_login;
CREATE DATABASE flask_login CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 然后重新运行初始化脚本
python init_db.py
```

### Q: 忘记了管理员密码
**A**: 删除数据库并重新初始化：
```bash
# 删除SQLite数据库文件
rm flask_login.db  # Linux/Mac
# 或在Windows资源管理器中删除 flask_login.db

# 然后重新运行初始化脚本
python init_db.py
```

### Q: 如何修改检测的置信度阈值
**A**: 编辑 `app/routes.py` 的 `process_frame` 函数，修改 `conf` 参数：
```python
results = model(img, conf=0.5)  # 改为 0.3-0.9
```

### Q: 想修改端口号
**A**: 在`.env`中修改：
```ini
FLASK_PORT=5000  # 修改为其他端口，如8000
```

---

## 📚 技术栈

### 核心框架
- **后端框架**: Flask 2.3.2
- **ORM**: SQLAlchemy 3.0.5
- **数据库**: SQLite（轻量级，文件存储）
- **会话管理**: Flask-Session 0.5.0
- **密码加密**: Bcrypt 4.0.1

### 前端技术
- **标记语言**: HTML5
- **样式**: CSS3（响应式设计，渐变背景）
- **交互**: Vanilla JavaScript（无框架依赖）
- **媒体**: HTML5 Canvas + getUserMedia API

### AI/ML 技术
- **目标检测**: YOLOv8（Ultralytics）
- **图像处理**: OpenCV（cv2）
- **数值计算**: NumPy
- **深度学习**: PyTorch
- **模型**: YOLOv8n（纳米版，仅50MB，速度快）

---

## 🎨 界面特性

- 现代化响应式设计
- 支持移动设备访问
- 美观的渐变背景
- 流畅的动画效果
- 详细的用户反馈提示

---

## 💡 扩展建议

### 认证功能扩展
1. **添加邮箱验证**: 用户注册时验证邮箱
2. **密码重置**: 实现忘记密码功能
3. **用户头像**: 允许用户上传头像
4. **OAuth登录**: 支持GitHub、Google等第三方登录

### 系统功能扩展
5. **操作日志**: 记录admin的操作历史
6. **权限细分**: 不同admin拥有不同权限
7. **API模式**: 改造为前后端分离架构（REST API）

### AI检测功能扩展
8. **检测历弯**: 保存用户的检测记录
9. **批量片图检测**: 上传多张图片进行批量分析
10. **自定义模型**: 训练自己的YOLOv8检测模型
11. **云端存储**: 保存检测结果和截图
12. **性能优化**: 转GPU加速，使用更大的YOLOv8模型
13. **多语言标签**: 支持不同语言的物体标签显示

---

## 📞 需要帮助？

- 阅读Flask官方文档: https://flask.palletsprojects.com/
- SQLAlchemy文档: https://docs.sqlalchemy.org/
- Bcrypt文档: https://pypi.org/project/bcrypt/

---

**祝你使用愉快！** 🎉
