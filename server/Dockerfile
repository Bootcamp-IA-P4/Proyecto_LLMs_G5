FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server /app/server
COPY client /app/client

EXPOSE 8000

RUN ls -lR /app/client
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"] 