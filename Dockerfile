# Stage 1 — builder
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    LANG=C.UTF-8

# Dependências do sistema necessárias para compilar pacotes e psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia apenas os arquivos de dependências primeiro (cache do Docker)
COPY requirements.txt /app/

# Instala poetry e exporta requirements.txt
RUN pip install --upgrade pip setuptools wheel

# Instala dependências em /opt/venv (isolado)
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . /app

# (Opcional) coletar static no builder (se suas settings permitirem sem variáveis runtime)
# RUN python manage.py collectstatic --noinput

# Stage 2 — runtime
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000

# Dependências runtime (bibliotecas do sistema)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório da aplicação
WORKDIR /app

# Copiar venv do builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar código da aplicação
COPY --from=builder /app /app

# Criar usuário não-root
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

# Expor porta
EXPOSE 8000

# Entrypoint que aplica migrations e collectstatic antes de iniciar o servidor
# OBS: Ajuste o caminho do WSGI (ex: "config.wsgi:application") conforme seu projeto.
COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

CMD ["/app/docker-entrypoint.sh"]
