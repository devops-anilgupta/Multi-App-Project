____________________________________________________________________________________
disallow-latest-tag.yaml
____________________________________________________________________________________
*** Kyverno policy that blocks Deployments/Pods using an image with the :latest tag.
    kubectl apply -f disallow-latest-tag.yaml

🔎 How this works
    !*:latest → means the image must not end with :latest.
    It will block Deployment/Pod creation if any container image uses latest.
    Works at both Pod and Deployment level.
____________________________________________________________________________________

____________________________________________________________________________________
Installation:
____________________________________________________________________________________
Here’s how you can install Kyverno using Helm step by step:

1. Add Kyverno Helm repo
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update

2. Create namespace for Kyverno
kubectl create namespace kyverno

3. Install Kyverno
helm install kyverno kyverno/kyverno -n kyverno

4. Verify installation

Check if the pods are running:

kubectl get pods -n kyverno


Expected output:

NAME                       READY   STATUS    RESTARTS   AGE
kyverno-abcdef1234-xyz     1/1     Running   0          1m
kyverno-abcdef1234-pqr     1/1     Running   0          1m
____________________________________________________________________________________

------------------------------------------------------------------------------------
apply kyverno policy and validate its status
------------------------------------------------------------------------------------
//Apply user-defined policy: 
PS D:\Kubernetes\multi-app-project-with-source\multi-app-project\helm\kyverno-policies> kubectl apply -f .\disallow-latest-tag.yaml

//Validate policy
PS D:\Kubernetes\multi-app-project-with-source\multi-app-project\helm\kyverno-policies> kubectl get cpol,pol -A
NAME                                           ADMISSION   BACKGROUND   READY   AGE   MESSAGE
clusterpolicy.kyverno.io/disallow-latest-tag   true        true         True    54s   Ready


//this is to create file, validate with blocked and allowed tag
1. kubectl apply -f disallow-latest-tag.yaml
2. kubectl run test-nginx --image=nginx:latest --restart=Never --dry-run=server   # blocked
3. kubectl run test-nginx-fixed --image=nginx:1.27.2 --restart=Never --dry-run=server  # allowed

2. kubectl run test-nginx --image=nginx:latest --restart=Never --dry-run=server   # blocked 
# blocked
when you run point #2, you would be seeing Error from server: admission webhook "validate.kyverno.svc-fail" denied the request: 
resource Pod/default/test-nginx was blocked due to the following policies

disallow-latest-tag:
  validate-image-tag: 'validation error: Using '':latest'' tag for container images
    is not allowed. Please
     use a fixed version tag. rule validate-image-tag failed
    at path /spec/containers/0/image/'


3. kubectl run test-nginx-fixed --image=nginx:1.27.2 --restart=Never --dry-run=server  # allowed
# allowed
PS D:\Kubernetes\multi-app-project-with-source\multi-app-project\helm\kyverno-policies> kubectl run test-nginx-fixed --image=nginx:1.27.2 --restart=Never --dry-run=server
pod/test-nginx-fixed created (server dry run)
------------------------------------------------------------------------------------s