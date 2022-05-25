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
      
  #### Configure kubectl context to access AKS cluster
  When you interact with an AKS cluster using the kubectl tool, a configuration file is used that defines cluster connection information. This configuration file is typically stored in ~/.kube/config. Multiple clusters can be defined in this kubeconfig file. You switch between clusters using the kubectl config use-context command.
  - The az aks get-credentials command lets you get the access credentials for an AKS cluster and merges them into the kubeconfig file. 
      `az aks get-credentials -n <myAKSCluster> -g <myResourceGroup>`
      * Better to save kubeconfig in Azure Key Vault
      
  - Using kubectl config get-contexts we'll be able to see all the clusters we've authenticated against:
      `kubectl config get-contexts`
      
  - We can switch context with below command to deploy applications in different enviornment like DEV / QA or Prod
      `kubectl config use-context <myAKSCluster>`

  
  #### Configure Helm (The Kubernetes package manager)
  - If helm is not installed, use below steps to install
      - wget https://get.helm.sh/helm-v3.8.2-linux-amd64.tar.gz
      - tar xvf helm-v3.8.2-linux-amd64.tar.gz
      - sudo mv linux-amd64/helm /usr/local/bin
  - Navigate to deploy folder (create if not available) of project
  - Run `helm create app`
  - Change values of values.yaml as per requirements
    
  #### Deploy to AKS using Helm
  - Run `helm install flaskapp ./app/` as we already set context of kubectl helm will use same context and deploy app in AKS.
  - verify by running `kubectl get pods`
  - Save your charts as .tgz with `helm package ./app/`
    
  #### Deploy to AKS using Kubectl
  - `helm template flaskapp ./app/ > flask-deployment.yaml` 
  - `kubectl apply -f flask-deployment.yaml`
  
  #### Deploy to AKS using Jenkins
  - Use `deploy/Jenkinsfile` to create CD pipeline in Jenkins
  
  #### Deploy to AKS using ArgoCD
  - Installing Argo CD
    -  ```kubectl create namespace argocd```
    -  ```kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml```
  - Install Argo CD CLI
    - `curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64`
    - `chmod +x /usr/local/bin/argocd`
  - Argo CD auto generated a password during the deployment. We need to get the Argo CD password so we can log into it. To get the password run the following:
    -  ```kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath=”{.data.password}” | base64 -d && echo```
  - Argo CD can be configured in three different ways: (In this example, I use the third method)
     1. using the GUI
     2. using the CLI
     3. Declarative Setup (Argo CD applications, projects and settings can be defined declaratively using Kubernetes manifests. These can be updated using kubectl apply, without needing to touch the argocd command-line tool). 
        - yaml files for argocd project and application created under deploy directory.
        - All resources, including Application and AppProject specs, have to be installed in the Argo CD namespace (by default argocd).
        - `kubectl -n argocd apply -f project.yaml`
        - `kubectl -n argocd apply -f application.yaml`
  
  
      
      
