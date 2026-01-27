FROM python:3.10.7-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache \
        gcc \
        musl-dev \
        python3-dev \
        libc-dev \
        libffi-dev \
        openssl-dev \
        pkgconfig \
        make \
        tzdata \
    && rm -rf /var/cache/apk/

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Local directory with project source
ENV DOCKYARD_SRC=.
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv
# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=$DOCKYARD_SRVHOME/
# Update the default application repository sources list

# Create application subdirectories
WORKDIR $DOCKYARD_SRVHOME

# Copy application source code to SRCDIR
COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ
# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r $DOCKYARD_SRVPROJ/requirements.txt --no-cache-dir
# Port to expose
EXPOSE 8000
# Copy entrypoint script into the image
WORKDIR $DOCKYARD_SRVPROJ

# Usando a imagem base do Python
FROM python:3.10.7-alpine

# Instalar dependências
RUN apk add --no-cache gcc musl-dev

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor a porta que o Gunicorn irá usar
EXPOSE 8000

# Comando para iniciar o Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "webrtcAPI.wsgi:application"]

