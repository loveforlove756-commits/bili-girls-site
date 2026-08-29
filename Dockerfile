# 自建部署用镜像：运行后即为纯 Streamlit 服务，无 Streamlit Cloud 平台外壳
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

# 绑定 0.0.0.0 并读取平台注入的 $PORT（未设置时默认 8501）
CMD ["sh", "-c", "streamlit run wz.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true"]
