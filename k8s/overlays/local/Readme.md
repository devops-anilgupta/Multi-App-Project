------------------------------------------------------------------------------------------------
🚀 Usage | Starting minikube, creating folder & providing appropriate permission
------------------------------------------------------------------------------------------------

Step 1:
//Make sure Minikube has /mnt/data & permission 
>> minikube status //Check minikube status, if stopped, start the minikube with the below command. 
>> minikube start //starting minikube
>> sudo mkdir -p /mnt/data
>> sudo chmod 777 /mnt/data
>> exit //exit minikube shell


Step 2: 
For local testing:
>> go to source code k8 folder in cmd
>> kubectl apply -k k8s/overlays/local

Step 3:
Run this to expose frontend/backend app on browser. 
>> minikube service dev-frontend -n dev
>> minikube service dev-backend -n dev

Step 4:
Go inside POD
>> kubectl exec -it dev-mysql-5559c9bf78-wbrjv -n dev -- /bin/sh
>> mysql -h 127.0.0.1 -u root -p //this is for mysql... enter password as rootpassword
>> kubectl run -it mysql-client --image=mysql:8.0 --rm --restart=Never -- mysql -h mysql.local.svc.cluster.local -utestuser -ptestpassword userdb

1. Start Minikube with Ingress Add-on
minikube start
minikube addons enable ingress


kubectl port-forward -n local deployment/frontend 3000:3000
kubectl port-forward -n local deployment/backend 5000:5000

------------------------------------------------------------------------------------------------

