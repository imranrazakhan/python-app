# Local Deployment
  - python3 -m venv .venv
  - source .venv/bin/activate 
  - pip install -r requirements.txt
  - docker build -t pythonflaskapp -f build/Dockerfile .
  - docker run -d -p 5000:5000 pythonflaskapp
  - curl http://localhost:5000
  - deactivate
  
# Azure Kubernetes Service(AKS) Deployment
  #### Prerequisites
    - For creation of Azure cloud resources, you will need to have a subscription that will allow you to create resources.
    - Create an Azure Kubernetes Service from Azure portal / Terraform.
    - Create an Azure Container Registry from Azure portal / Terraform.
    - These tools are required:
      - Azure CLI tool (az): command line tool that interacts with Azure API.
      - Kubernetes client tool (kubectl): command line tool that interacts with Kubernetes API
      - Helm (helm): command line tool for “templating and sharing Kubernetes manifests”  that are bundled as Helm chart packages.
  
  #### Upload the image to Azure Container Registry (ACR)
    - *Log in to a registry*
        - `az login`
        - `az acr login --name myregistry`
    - *Tag your local image to be pushed to ACR with:*
        - `docker tag pythonflaskapp [myAcrName].azurecr.io/pythonflaskapp:v1`
    - *Push the image to ACR with:*
        - `docker push [myAcrName].azurecr.io/pythonflaskapp:v1`

  #### Configure ACR integration for AKS clusters
    We’re almost ready to deploy this thing—we just need to give our cluster permission to access the container registry.
      -  `az aks update -n myAKSCluster -g myResourceGroup --attach-acr <myAcrName>`

  
# Install Helm
- Prerequisite
  - A Linux machine with Kubectl and docker installed. 
- wget https://get.helm.sh/helm-v3.8.2-linux-amd64.tar.gz
- tar xvf helm-v3.8.2-linux-amd64.tar.gz
- sudo mv linux-amd64/helm /usr/local/bin
