# ticketing-service description
This is a service that manages events and its tickets.

# deployment

# Inside the ticketing folder
# To build the latest images and send them to DETI repository:

    sudo docker build -f Dockerfile.app -t registry.deti:5000/ticketing/app-ticketing:202206221407 .
    sudo docker build -f Dockerfile.nginx -t registry.deti:5000/ticketing/nginx-ticketing:202206211512 .
    sudo docker push registry.deti:5000/ticketing/app-ticketing:202206221407
    sudo docker push registry.deti:5000/ticketing/nginx-ticketing:202206211512

# To deploy the services to Kubernetes cluster, you need to follow these commands
# To ensure there is no previous deployment there

    kubectl delete -f deployment-db.yaml
    kubectl delete -f deployment-conf.yaml
    kubectl delete -f deployment-app.yaml
    kubectl delete -f deployment-nginx.yaml

# To create the secret used by the app to connect to the database

    bash create.sh

# To apply the deployment of all the project components

    kubectl apply -f deployment-db.yaml
    kubectl apply -f deployment-conf.yaml
    kubectl apply -f deployment-app.yaml
    kubectl apply -f deployment-nginx.yaml

# yaml files explanation

deployment-db.yaml launches the Deployment, Service and PersistentVolumeClaim for the Postgres Database
deployment-conf.yaml launches the ConfigMap with the credentials used by the Database
deployment-app.yaml launches the Deployment and Service for the main application
deployment-nginx.yaml launches the Deployment, Service and Ingress for NGINX