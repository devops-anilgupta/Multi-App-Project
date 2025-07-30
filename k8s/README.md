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


Name prefix/namespace	dev-backend, dev-frontend	prod-backend, prod-frontend
