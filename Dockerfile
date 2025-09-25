# Stage 1 — builder
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
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
# ----------------------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000

# Instalar runtime libs mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar virtualenv e aplicação do builder
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

# Definir permissões e usuário não-root (chmod e chown executados como root)
# Ajuste o nome do entrypoint se for diferente
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app \
    && chmod +x /app/docker-entrypoint.sh || true

# Trocar para usuário não-root
USER appuser

EXPOSE 8000

# OBS: ajuste o WSGI_MODULE caso seu wsgi esteja em outro pacote.
# Exemplo abaixo usa: sorteadorcredilab.wsgi:application
CMD ["/app/docker-entrypoint.sh"]
