"""
数据库初始化脚本
首次运行时创建所有表，并插入初始的管理员账号和测试用户
"""
import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User

load_dotenv()

def init_database():
    """初始化数据库"""
    app = create_app()
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("✓ 数据库表创建成功")
        
        # 检查是否已存在管理员
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("✓ 默认管理员账号创建成功")
            print("   用户名: admin")
            print("   密码: admin123")
        else:
            print("✓ 管理员账号已存在，跳过创建")
        
        # 检查是否已存在测试用户
        test_user = User.query.filter_by(username='user').first()
        if not test_user:
            test_user = User(
                username='user',
                email='user@example.com',
                role='user'
            )
            test_user.set_password('user123')
            db.session.add(test_user)
            print("✓ 默认测试用户创建成功")
            print("   用户名: user")
            print("   密码: user123")
        else:
            print("✓ 测试用户已存在，跳过创建")
        
        # 再添加几个测试用户
        for i in range(2, 6):
            test_name = f'testuser{i}'
            if not User.query.filter_by(username=test_name).first():
                new_user = User(
                    username=test_name,
                    email=f'{test_name}@example.com',
                    role='user'
                )
                new_user.set_password('password123')
                db.session.add(new_user)
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("✓ 数据库初始化完成！")
        print("="*50)
        print("\n😊 可用的测试账户：")
        print("\n【管理员账号】")
        print("  用户名: admin")
        print("  密码: admin123")
        print("\n【普通用户账号】")
        print("  用户名: user")
        print("  密码: user123")
        print("  用户名: testuser2-5")
        print("  密码: password123")
        print("\n🚀 接下来请运行: python run.py")
        print("="*50)

if __name__ == '__main__':
    init_database()
