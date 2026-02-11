FROM ubuntu:24.04

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Criar usuário sem conflito de GID
RUN useradd -m filme

# Instalar dependências
RUN apt update && \
    apt install -y software-properties-common python3 python3-pip gunicorn && \
    apt clean

RUN pip3 install Flask geojson psycopg2-binary Flask-Cors python-dotenv \
    pipenv virtualenv virtualenv-clone uwsgi requests

WORKDIR /app
COPY . .

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

USER filme

CMD ["gunicorn", "myapp:app", "--bind", "0.0.0.0:8080"]

