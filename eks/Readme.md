2. Create the IAM policy from the file
>> aws iam create-policy --policy-name eks-admin-full-access --policy-document file://eks-admin-policy.json
Note the output policy ARN this will be like this --> "arn:aws:iam::816150604527:policy/eks-admin-full-access"




3. Attach the policy to your IAM user or role
For user: 
>> aws iam attach-user-policy --user-name dev-user1 --policy-arn <<Paste ARN from step 2 here>>
    
For example: 
>> aws iam attach-user-policy --user-name dev-user1 --policy-arn arn:aws:iam::816150604527:policy/eks-admin-full-access



4. For role:
aws iam attach-role-policy --role-name YOUR_ROLE_NAME --policy-arn arn:aws:iam::816150604527:policy/eks-admin-full-access


5. Create the EKS cluster IAM role
aws iam create-role --role-name eks-cluster-role --assume-role-policy-document file://eks-cluster-trust-policy.json


6. Attach AWS-managed policies to the cluster role
>> aws iam attach-role-policy --role-name eks-cluster-role --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
>> aws iam attach-role-policy --role-name eks-cluster-role --policy-arn arn:aws:iam::aws:policy/AmazonEKSServicePolicy


7. Get the ARN of the cluster role
>> aws iam get-role --role-name eks-cluster-role --query 'Role.Arn' --output text


8. This is to use existing VPC, subnets, AZs.. It shows you the table wherein it will list the subnets, azs which can later change in below step 9.
>> aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-080e049dd2e198c43" --region us-east-1 --query "Subnets[].{ID:SubnetId,AZ:AvailabilityZone,CIDR:CidrBlock}" --output table


9. Create the EKS cluster (replace <ROLE_ARN>, subnets, and security groups)
>> eksctl create cluster -f eks-cluster-fargate-dev.yaml --verbose 4


10. Delete the EKS cluster if you don't want to be billed
>> eksctl delete cluster --name multi-app-fargate-dev --region us-east-1 


11. ✅ Update kubeconfig to Access the EKS Cluster. This will configure kubectl to connect to your EKS cluster.
>> aws eks --region us-east-1 update-kubeconfig --name your-cluster-name
once you delete your EKS cluster, the kubeconfig that pointed to that EKS cluster will no longer work but:
✅ To confirm what kubectl is using now 
>> kubectl config current-context //If it shows something like minikube, then your kubeconfig has indeed defaulted back to your local Minikube cluster.

🔁 If needed, switch to Minikube explicitly:
>> kubectl config use-context minikube


For example:
D:\Kubernetes\multi-app-project-with-source\multi-app-project\eks>aws eks --region us-east-1 update-kubeconfig --name <<multi-app-fargate-dev>>
Added new context arn:aws:eks:us-east-1:816150604527:cluster/multi-app-fargate-dev to C:\Users\Dell\.kube\config

Test it:
kubectl get nodes
You should see Fargate or EC2 nodes, depending on your setup. 




Diagram:
+---------------------------+
| 1. Create eks-admin-policy.json (custom policy for EKS + Secrets Manager)  |
+---------------------------+
            |
            v
+---------------------------+
| 2. Run `aws iam create-policy` to create admin policy                     |
+---------------------------+
            |
            v
+---------------------------+
| 3. Attach policy to your IAM User/Role using `attach-user-policy` or      |
|    `attach-role-policy`                                                   |
+---------------------------+
            |
            v
+---------------------------+
| 4. Create eks-cluster-trust-policy.json (trust policy for EKS role)       |
+---------------------------+
            |
            v
+---------------------------+
| 5. Create EKS cluster role using `aws iam create-role`                    |
+---------------------------+
            |
            v
+---------------------------+
| 6. Attach AWS managed policies to EKS cluster role                        |
|    (`AmazonEKSClusterPolicy` and `AmazonEKSServicePolicy`)                |
+---------------------------+
            |
            v
+---------------------------+
| 7. Get ARN of the EKS cluster role                                        |
+---------------------------+
            |
            v
+---------------------------+
| 8. Create EKS cluster with `aws eks create-cluster` using the role ARN    |
+---------------------------+
            |
            v
+---------------------------+
| 9. (Optional) Create Fargate profile to run pods serverlessly              |
+---------------------------+
