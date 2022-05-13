# Local 
  - python3 -m venv .venv
  - source .venv/bin/activate 
  - docker build -t testflask -f build/Dockerfile .
  - docker run -d -p 5000:5000 testflask
  - curl http://localhost:5000
  - deactivate

# Upload the image to Azure Container Registry
- *Prerequisites
  - Azure Subscription
  - Create an Azure Container Registry from Azure portal / Terraform.
  - You’ll also need Azure CLI (command line interface) installed
- *Log in to a registry
  - az login
  - az acr login --name myregistry
- *Tag your local image to be pushed to ACR with: 
  - docker tag pythonflaskapp [myAcrName].azurecr.io/pythonflaskapp:v1
- *Push the image to ACR with: 
  - docker push [myAcrName].azurecr.io/pythonflaskapp:v1

  
# Install Helm
- Prerequisite
  - A Linux machine with Kubectl and docker installed. 
- wget https://get.helm.sh/helm-v3.8.2-linux-amd64.tar.gz
- tar xvf helm-v3.8.2-linux-amd64.tar.gz
- sudo mv linux-amd64/helm /usr/local/bin
