📁 Why separate environment folders (dev, uat, etc.) are created?
Each environment needs slightly different configurations, such as:
------------------------------------------------------------------------------------------
Property	                            Dev	                Prod
------------------------------------------------------------------------------------------
Number of replicas	                    1	                3
Image tag	                            dev	                prod
Resource limits	Low                 (for testing)	        High (for performance)
Secrets or env vars	                Dev DB credentials	    Prod DB credentials
------------------------------------------------------------------------------------------

kubectl apply -k overlays/dev      # Deploys dev environment
kubectl apply -k overlays/prod     # Deploys production environment

___________________________________________________________________________________________
So, if your MySQL service is named mysql in namespace local, the correct hostname is:
___________________________________________________________________________________________
**** When you create a Service in Kubernetes, it automatically gets a DNS record inside the cluster based on:
<service-name>.<namespace>.svc.cluster.local
___________________________________________________________________________________________

Name prefix/namespace	dev-backend, dev-frontend	prod-backend, prod-frontend

>> kubectl exec -it pod/mysql-d789cd997-lmv4m -n local --  mysql -h mysql -u testuser -p userdb

-----------------------------------------------------------
*** [Kyverno] is like AWS Config to control cluster level policy in kubernetes files. ***

- It ensures validate k8 files created.
- It does not allow to create file until condition written in kyverno satisfied.  

*** Install Kyverno using Helm ***

- helm repo add kyverno https://kyverno.github.io/kyverno/
- helm repo update

//Installed the kyverno with namespace kyverno
- helm install kyverno kyverno/kyverno -n kyverno --create-namespace

//Validate namespace, this ensure it installed perfectly: 
kubectl get ns
-----------------------------------------------------------