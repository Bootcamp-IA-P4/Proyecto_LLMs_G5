FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server /app/server
COPY client /app/client

RUN apt-get update && apt-get install -y --no-install-recommends iputils-ping curl ca-certificates && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]