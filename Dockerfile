FROM ubuntu:24.04

# Configuração do fuso horário
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Configuração de usuário
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN if getent group filme ; then groupdel filme; fi
RUN groupadd -g ${GROUP_ID} filme
RUN useradd -l -u ${USER_ID} -g filme filme
RUN install -d -m 0775 -o filme -g filme /home/filme

# Atualização do sistema e instalação de dependências
RUN apt update -y && apt upgrade -y
RUN apt-get install -y software-properties-common python3.13 python3-pip gunicorn
RUN pip3 install Flask geojson psycopg2-binary Flask-Cors python-dotenv pipenv virtualenv virtualenv-clone uwsgi requests

# Define a pasta de trabalho
WORKDIR /app

# Copia o restante da aplicação para o contêiner
COPY . .

# Define a variável de ambiente para produção
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV APP_FLASK_DEBUG=True
ENV APP_FLASK_PORT=8080
ENV APP_FLASK_HOST=0.0.0.0

# Exposição da porta
EXPOSE 8080

# Muda para o usuário não-root
USER filme

# Comando de inicialização
CMD ["gunicorn", "myapp:app", "--bind", "0.0.0.0:8080"]
