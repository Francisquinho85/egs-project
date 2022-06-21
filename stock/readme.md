STOCK

To deploy:
 - sudo docker build -f Dockerfile.app -t registry.deti:5000/ticketing/app-stock-ticketing:2022062110
 - sudo docker build -f Dockerfile.nginx -t registry.deti:5000/ticketing/nginx-stock-ticketing:2022062110
 - sudo docker push registry.deti:5000/ticketing/app-stock-ticketing:2022062110
 - sudo docker push registry.deti:5000/ticketing/nginx-stock-ticketing:2022062110
 - kubectl delete -f deployment-conf.yaml
 - kubectl delete -f deployment-db.yaml
 - kubectl delete -f deployment-app.yaml 
 - kubectl delete -f deployment-nginx.yaml
 - kubectl apply -f deployment-conf.yaml
 - kubectl apply -f deployment-db.yaml
 - kubectl apply -f deployment-app.yaml 
 - kubectl apply -f deployment-nginx.yaml