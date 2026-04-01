/**
 * Flask登录系统 - 主要JavaScript文件
 */

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * 初始化应用
 */
function initializeApp() {
    // 初始化提示信息自动隐藏
    initializeAlerts();
    
    // 初始化表单验证
    initializeFormValidation();
    
    // 初始化演示账号快速填充（仅在登录页面）
    if (document.getElementById('username')) {
        initializeDemoAccounts();
    }
}

/**
 * 初始化提示信息 - 3秒后自动隐藏
 */
function initializeAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // 为每个成功和信息提示添加自动隐藏
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(() => {
                alert.style.display = 'none';
            }, 3000);
        }
    });
}

/**
 * 初始化表单验证
 */
function initializeFormValidation() {
    // 验证密码确认匹配
    const passwordInput = document.getElementById('new_password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    
    if (passwordInput && confirmPasswordInput) {
        confirmPasswordInput.addEventListener('change', function() {
            if (passwordInput.value !== confirmPasswordInput.value) {
                confirmPasswordInput.setCustomValidity('密码不匹配');
            } else {
                confirmPasswordInput.setCustomValidity('');
            }
        });
    }
}

/**
 * 登录页面演示账号快速填充
 */
function initializeDemoAccounts() {
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    if (!usernameInput || !passwordInput) return;
    
    // 获取表单
    const form = usernameInput.closest('form');
    if (!form) return;
    
    // 添加演示账号点击处理
    const accountItems = document.querySelectorAll('.account-item');
    accountItems.forEach((item, index) => {
        item.style.cursor = 'pointer';
        item.addEventListener('click', function() {
            if (index === 0) {
                // 管理员账号
                usernameInput.value = 'admin';
                passwordInput.value = 'admin123';
            } else {
                // 普通用户账号
                usernameInput.value = 'user';
                passwordInput.value = 'user123';
            }
            usernameInput.focus();
        });
        
        // 悬停效果
        item.addEventListener('mouseenter', function() {
            this.style.background = '#e8eef7';
            this.style.transform = 'translateX(5px)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.background = '#f8f9fa';
            this.style.transform = 'translateX(0)';
        });
    });
}

/**
 * 删除确认对话框
 */
function confirmDelete(username) {
    return confirm(`确定要删除用户 "${username}" 吗？此操作无法撤销。`);
}

/**
 * 显示加载动画
 */
function showLoading() {
    const loader = document.createElement('div');
    loader.id = 'loading-overlay';
    loader.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    `;
    loader.innerHTML = '<div style="color: white; font-size: 20px;">加载中...</div>';
    document.body.appendChild(loader);
}

/**
 * 隐藏加载动画
 */
function hideLoading() {
    const loader = document.getElementById('loading-overlay');
    if (loader) {
        loader.remove();
    }
}

/**
 * 导出用户数据（示例功能）
 */
function exportUserData() {
    console.log('导出用户数据功能');
}
