# 官方 Python 镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制依赖清单并安装
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . /app

# 暴露默认端口
EXPOSE 5000

# 默认环境变量（可在 docker run 或 compose 中覆盖）
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False

# 启动命令
CMD ["python", "run.py"]
