# housekeeping_pods
To get the status of all the pods running in a cluster

You need to simply execute the house_keeping_pods.py file in the Kubernetes Master Node.

Command: python3 house_keeping_pods.py

# Objecctive:
When this file is executed it gets all the pods in the cluster. Loops through each of these clusters and evalueates 3 rules mentioned below. Finally prints out the evaluated rules.

# Rules:
1. Image_name has 'bitnami/' as prefix, if yes True, else False
2. Pod Label has 'team' as a keyword in it. If yes True, else False
3. Checks if the pod has not run for more than 7 days. If yes then True, else False.
