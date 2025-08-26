1️⃣ Install a Helm chart
helm install <release-name> <chart-path> -n <namespace>


Example:

helm install backend ./backend-chart -n dev


Output:

NAME: backend
LAST DEPLOYED: Sun Aug 18 01:10:00 2025
NAMESPACE: dev
STATUS: deployed

2️⃣ Upgrade / Install if exists
helm upgrade --install <release-name> <chart-path> -n <namespace>


Example:

helm upgrade --install backend ./backend-chart -n dev

3️⃣ List Helm releases

In a specific namespace:

helm list -n dev


Output:

NAME     	NAMESPACE	REVISION	STATUS  	CHART          	APP VERSION
backend  	dev      	1       	deployed	backend-0.1.0  	1.0


Across all namespaces:

helm list --all-namespaces


Output:

NAME     	NAMESPACE	REVISION	STATUS  	CHART
backend  	dev      	1       	deployed	backend-0.1.0
frontend 	default  	1       	deployed	frontend-0.1.0
mysql    	db       	1       	deployed	mysql-0.1.0

4️⃣ Get release details
helm status <release-name> -n <namespace>


Example:

helm status backend -n dev


Output:

NAME: backend
LAST DEPLOYED: Sun Aug 18 01:10:00 2025
NAMESPACE: dev
STATUS: deployed
REVISION: 1
CHART: backend-0.1.0
APP VERSION: 1.0

5️⃣ Show release values
helm get values <release-name> -n <namespace>


Shows values.yaml used for deployment.

Add -a to see all values including defaults:

helm get values backend -n dev -a

6️⃣ Show manifest (all resources Helm will create)
helm get manifest <release-name> -n <namespace>

7️⃣ Delete / Uninstall release
helm uninstall <release-name> -n <namespace>


Example:

helm uninstall backend -n dev


Deletes all pods, deployments, services, PVCs, etc. created by that release.

8️⃣ Rollback release
helm rollback <release-name> <revision> -n <namespace>


Check history first:

helm history backend -n dev

9️⃣ Check pods created by a Helm release (one-liner)

Helm automatically labels resources with app.kubernetes.io/instance=<release-name>.

kubectl get pods --all-namespaces -l app.kubernetes.io/instance=<release-name>


Example:

kubectl get pods --all-namespaces -l app.kubernetes.io/instance=backend


Output:

NAMESPACE   NAME                       READY   STATUS    RESTARTS   AGE
dev         backend-6d4f7f7b9c-abc12   1/1     Running   0          10m


✅ This shows the namespace and all pods created by that Helm release.

10️⃣ Extra Tips

Always specify the namespace with -n <namespace> to avoid accidentally deploying in default.

To see which Helm release created a pod, check its label:

kubectl get pod <pod-name> -n <namespace> --show-labels


Output example:

NAME                       READY   STATUS    LABELS
backend-6d4f7f7b9c-abc12   1/1     Running   app.kubernetes.io/instance=backend,app.kubernetes.io/name=backend