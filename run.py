"""
Flask应用启动脚本
"""
import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入创建app的工厂函数
from app import create_app

# 创建应用
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Flask服务器启动")
    print(f"📍 访问地址: http://localhost:{port}")
    print(f"🔑 登录账号:")
    print(f"   管理员: admin / admin123")
    print(f"   用户: user / user123")
    print(f"按 Ctrl+C 停止服务器\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
