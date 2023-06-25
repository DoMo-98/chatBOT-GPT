# Utilizamos la imagen base de Python 3.11.4 con Alpine 3.18
FROM python:3.11.4-alpine3.18

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos los archivos del directorio actual al contenedor
COPY . /app

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# Ejecutamos el programa Python
CMD ["python", "main.py"]

