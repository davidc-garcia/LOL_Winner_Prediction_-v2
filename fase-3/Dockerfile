# Usa una imagen base de Python
FROM python

# Instala las dependencias del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al directorio de trabajo del contenedor
COPY . /app

# Define el comando para ejecutar tu aplicación Flask
CMD flask --app myapirest.py run --host=0.0.0.0
