#!/bin/bash

# Define variables
IMAGE_NAME="examen3"  # Cambia esto por el nombre que desees para tu imagen
CONTAINER_NAME="pagina_web"  # Cambia esto por el nombre que desees para tu contenedor

# Construir la imagen
echo "Construyendo la imagen..."
docker build -t $IMAGE_NAME .

# Ejecutar el contenedor
echo "Ejecutando el contenedor..."
docker run -d --name $CONTAINER_NAME -p 80:80 $IMAGE_NAME

# Mensaje final
echo "La imagen y el contenedor se han creado y están en ejecución."
echo "Puedes acceder a tu página web en http://localhost"
