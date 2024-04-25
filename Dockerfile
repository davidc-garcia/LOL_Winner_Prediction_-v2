# Usa una imagen base de Python
FROM python

# Instala las dependencias del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala git para poder clonar el repositorio
RUN apt-get update && apt-get install -y git

# Clona el repositorio de GitHub que contiene la carpeta "fase-2"
RUN git clone https://github.com/davidc-garcia/LOL_Winner_Prediction_-v2.git

# Copia la carpeta "fase-2" del repositorio clonado al directorio de trabajo del contenedor
COPY /fase-2 /app
