# Dockerfile multistage para Django + Poetry (Python 3.12)
# Ajuste WSGI_MODULE abaixo conforme o caminho do seu projeto Django, ex: "sorteadorcredilab.wsgi:application"

# -----------------------
# Stage 1: builder
# -----------------------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    TZ=UTC

# Dependências do sistema para build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Garantir pip/setuptools compatíveis e instalar poetry
RUN python -m pip install --upgrade pip setuptools wheel

# Criar virtualenv e instalar dependências
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação (agora que dependências estão instaladas)
COPY . /app

# -----------------------
# Stage 2: runtime
# -----------------------
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
