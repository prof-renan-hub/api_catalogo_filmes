FROM python:3.13-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Criar usuário não-root
RUN useradd -m filme

# Diretório da aplicação
WORKDIR /app

# Copiar dependências primeiro (melhora cache)
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar resto do projeto
COPY . .

# Mudar para usuário não-root
USER filme

EXPOSE 8080

CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:$PORT"]
