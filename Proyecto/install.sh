#!/bin/bash

# Actualiza el sistema
sudo apt update -y

# Descargar e instalar AWS CLI
sudo apt install curl
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip

# Descargar e instalar Terraform
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update
sudo apt install terraform

# Configura AWS CLI automáticamente
aws configure set aws_access_key_id "ASIA3LSDABXJ24X3YFO6"
aws configure set aws_secret_access_key "fdR9pHlpgEjm8NetVYQFcA5cOMbe4vTEwxU+Uhc3"
aws configure set region "us-east-1"
aws configure set output "json"

# Reemplaza el archivo de credenciales
CREDENTIALS_FILE="$HOME/.aws/credentials"
echo "[default]" > $CREDENTIALS_FILE
echo "aws_access_key_id=ASIA5DUV7WDEJSUN4CJY" >> $CREDENTIALS_FILE
echo "aws_secret_access_key=ogfSSlmNBajA0qV4t6tfCWGKmkbIrH0u46HN6fLg" >> $CREDENTIALS_FILE
echo "aws_session_token=IQoJb3JpZ2luX2VjEGAaCXVzLXdlc3QtMiJHMEUCIFCRPVjGjGYfDpdOb2pJ2/zlDLWDOjXSijiHkdUG8oeNAiEA1HmfpXyp22/reABYacwWpHjaJqzvfDWjyOpbcp6kwx0qsQII2f//////////ARACGgw5MDExODM5NDI4NTYiDDsrDppoNr3gEUxNEiqFApkVNAUriu9u6xwZh3ZuiEgi+IcGRDeV+u3Ks5sE6VUF3pPqoy2vugI9ZQqreGoIFnaYlf0itYMtOLkdheqNJy4nPvlpm04IeSXe0kMU6WnBOtjbVx9gR20wvgudZCTSFBRbqTgk7gHwNw+Qm5T7tg8mw+WaX70yOuYZRVImb+nAoroHtc6Wi1gAxfnKGh4nKgRu1JDc+1oOL5wsuKTHn4Z19ifrsHgmDirQSoByCYyntXyDsZq716BA7qngN2e4qaHVzgqr4uBicqb4yyYDSd8L59CeUzsPgmKtlCD6hkxrtzhIlmW90KGax2k1diY8KQbizTpKQLlQwYmpCwYbLSvmdHq5STCSvZ65BjqdAdJcLgitvNGeKjnHdRgqAboXDcR01GyR9enLYvsMuTUQpM2p5JgCXPd3Aaz9P+CmvHyD7FTAWxlyPPItO92LVwbpoGB7crwa8V0NEPmtFy9n3Xh4HAPj9FTFnkm8XFrp5tNcBBHAQIfGg7xrJ+HfdVbGCjA6jLZXp7eyhSTM3mwFtPVa61jEKf8mJlj8XU+74oRaZ9ag2INtz8m5xhs=" >> $CREDENTIALS_FILE

#Iniciar el terraform
cd examen3
cd Proyecto
terraform init
terraform plan
terraform apply -auto-approve



