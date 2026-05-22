
FROM python:3.11-alpine AS builder

WORKDIR /install

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --prefix=/install -r /requirements.txt

FROM python:3.11-alpine

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . /app


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000


CMD ["uvicorn", "app:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]