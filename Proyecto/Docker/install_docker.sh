# Actualiza el sistema
echo "Actualizando el sistema..."
sudo apt update -y

# Elimina paquetes existentes de Docker
echo "Eliminando versiones anteriores de Docker..."
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
    sudo apt-get remove -y $pkg
done

# Instala dependencias necesarias
echo "Instalando dependencias necesarias..."
sudo apt-get install -y apt-transport-https ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Añadir el repositorio a Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Instala Docker
echo "Instalando Docker..."
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verifica que Docker esté instalado correctamente
echo "Verificando la instalación de Docker..."
sudo systemctl status docker

# Inicia el servicio de Docker
echo "Iniciando el servicio de Docker..."
sudo service docker start

# Agregar el usuario actual al grupo 'docker'
echo "Agregando el usuario al grupo 'docker'..."
sudo groupadd docker
sudo usermod -aG docker $USER

echo "Docker instalado y servicio iniciado correctamente."
echo "Para poder ejecutar Docker sin 'sudo', cierra y vuelve a abrir la terminal o ejecuta 'newgrp docker'."
