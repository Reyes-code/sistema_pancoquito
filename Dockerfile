FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python manage.py migrate && gunicorn gestion_pedidos.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120"]