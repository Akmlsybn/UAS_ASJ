FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
COPY app.py .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["flask", "--app", "app.py", "run", "--host=0.0.0.0", "--port=5000"]
