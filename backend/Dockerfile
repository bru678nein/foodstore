FROM python:3.12-slim

WORKDIR /codigo

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requisitos.txt .
RUN pip install --no-cache-dir -r requisitos.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.principal:aplicacion", "--host", "0.0.0.0", "--port", "8000"]
