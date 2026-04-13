FROM python:3.12-slim AS base

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

FROM base AS test
CMD ["sh", "-c", "pytest tests/unit && python scripts/run_with_server.py --server-cmd 'python app.py' --target-url 'http://127.0.0.1:5000/health' -- behave -f pretty features"]

FROM base AS runtime
EXPOSE 5000
CMD ["python", "app.py"]
