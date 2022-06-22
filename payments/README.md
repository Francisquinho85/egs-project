README.md# payments-service description
This is a service that manages payments.

# Deployment
## To build the latest images and send them to DETI repository(inside the payments folder):

    sudo docker build -f Dockerfile.app -t registry.deti:5000/ticketing/app-payments:2024 .
    sudo docker build -f Dockerfile.nginx -t registry.deti:5000/ticketing/nginx-payments:2024 .
    sudo docker push registry.deti:5000/ticketing/app-payments:2024
    sudo docker push registry.deti:5000/ticketing/nginx-payments:2024

## To deploy the services to Kubernetes cluster, you need to follow these commands
### To ensure there is no previous deployment there

    kubectl delete -f deployment-db.yaml
    kubectl delete -f deployment-conf.yaml
    kubectl delete -f deployment-app.yaml
    kubectl delete -f deployment-nginx.yaml

### To create the secret used by the app to connect to the database

    bash create.sh

### To apply the deployment of all the project components

    kubectl apply -f deployment-db.yaml
    kubectl apply -f deployment-conf.yaml
    kubectl apply -f deployment-app.yaml
    kubectl apply -f deployment-nginx.yaml

# yaml files explanation

deployment-db.yaml launches the Deployment, Service and PersistentVolumeClaim for the Postgres Database </br>
deployment-conf.yaml launches the ConfigMap with the credentials used by the Database </br>
deployment-app.yaml launches the Deployment and Service for the main application </br>
deployment-nginx.yaml launches the Deployment, Service and Ingress for NGINX