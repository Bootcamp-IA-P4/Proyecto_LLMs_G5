# Usa una imagen base ligera con Python
FROM python:3.12.0

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de Streamlit
EXPOSE 8501

# Comando para ejecutar la app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]