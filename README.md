# Flask登录系统 - 运行指南

## 📋 项目概览

这是一个完整的Flask Web应用，支持用户和管理员双端登录，包含：
- ✅ 用户/管理员统一登录界面
- ✅ 用户个人中心（修改密码）
- ✅ 管理员后台（用户增删改查）
- ✅ Session会话管理
- ✅ Bcrypt密码加密
- ✅ MySQL数据库

---

## 🚀 快速开始

### 第1步：创建MySQL数据库

打开MySQL客户端（或MySQL Workbench），执行：

```sql
CREATE DATABASE flask_login CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 第2步：安装Python依赖

在项目根目录打开终端，运行：

```bash
pip install -r requirements.txt
```

或者逐个安装（如果pip有问题）：

```bash
pip install Flask==2.3.2
pip install Flask-SQLAlchemy==3.0.5
pip install Flask-Session==0.5.0
pip install bcrypt==4.0.1
pip install python-dotenv==1.0.0
pip install PyMySQL==1.1.0
```

### 第3步：配置环境变量

编辑 `.env` 文件，根据你的MySQL配置修改：

```ini
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here
DB_USER=root           # 你的MySQL用户名
DB_PASSWORD=password   # 你的MySQL密码
DB_HOST=localhost      # MySQL主机
DB_NAME=flask_login    # 数据库名（上面创建的）
```

### 第4步：初始化数据库

运行初始化脚本，创建表并插入测试数据：

```bash
python init_db.py
```

你会看到类似输出：

```
✓ 数据库表创建成功
✓ 默认管理员账号创建成功
✓ 默认测试用户创建成功
...
✓ 数据库初始化完成！

😊 可用的测试账户：
【管理员账号】
  用户名: admin
  密码: admin123

【普通用户账号】
  用户名: user
  密码: user123
```

### 第5步：启动Flask应用

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
4. 点击"登出"退出登录

#### 👨‍💼 管理员流程：
1. 用户名：`admin`，密码：`admin123`
2. 登录后进入管理员后台
3. 查看统计数据（用户数、管理员数等）
4. 进入"用户管理"页面
5. 可以：
   - ➕ 添加新用户
   - ✏️ 编辑用户（邮箱、角色、密码）
   - 🗑️ 删除用户
6. 点击"登出"退出登录

---

## 📁 项目结构

```
test/
├── app/
│   ├── __init__.py        # 应用工厂
│   ├── config.py          # 配置管理
│   ├── models.py          # 数据库模型（User）
│   ├── routes.py          # 所有路由
│   ├── auth.py            # 认证装饰器
│   └── utils.py           # 工具函数
├── templates/             # HTML模板
│   ├── base.html          # 基础模板
│   ├── login.html         # 登录页面
│   ├── user_profile.html  # 用户中心
│   ├── admin_dashboard.html  # 管理员首页
│   ├── admin_users.html   # 用户管理
│   ├── admin_add_user.html    # 添加用户
│   └── admin_edit_user.html   # 编辑用户
├── static/
│   ├── css/
│   │   └── style.css      # 全局样式
│   └── js/
│       └── main.js        # JavaScript交互
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
- 使用MySQL存储用户数据
- SQLAlchemy ORM进行数据库操作
- 自动时间戳（created_at, updated_at）

---

## 🐛 常见问题

### Q: 无法连接到MySQL
**A**: 检查以下几点：
1. MySQL服务是否启动
2. `.env`文件中的数据库配置是否正确
3. 用户名和密码是否正确
4. 数据库 `flask_login` 是否已创建

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

### Q: 想修改端口号
**A**: 在`.env`中修改：
```ini
FLASK_PORT=5000  # 修改为其他端口，如8000
```

---

## 📚 技术栈

- **后端框架**: Flask 2.3.2
- **ORM**: SQLAlchemy 3.0.5
- **数据库**: MySQL + PyMySQL
- **会话管理**: Flask-Session 0.5.0
- **密码加密**: Bcrypt 4.0.1
- **前端**: HTML5 + CSS3 + Vanilla JavaScript

---

## 🎨 界面特性

- 现代化响应式设计
- 支持移动设备访问
- 美观的渐变背景
- 流畅的动画效果
- 详细的用户反馈提示

---

## 💡 扩展建议

1. **添加邮箱验证**: 用户注册时验证邮箱
2. **密码重置**: 实现忘记密码功能
3. **用户头像**: 允许用户上传头像
4. **操作日志**: 记录admin的操作历史
5. **权限细分**: 不同admin拥有不同权限
6. **API模式**: 改造为前后端分离架构（REST API）

---

## 📞 需要帮助？

- 阅读Flask官方文档: https://flask.palletsprojects.com/
- SQLAlchemy文档: https://docs.sqlalchemy.org/
- Bcrypt文档: https://pypi.org/project/bcrypt/

---

**祝你使用愉快！** 🎉
