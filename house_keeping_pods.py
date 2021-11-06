from kubernetes import client, config
from datetime import datetime, timedelta

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()
ret = v1.list_pod_for_all_namespaces(watch=False)

# we are looping through all the pods andd extracting required fields for rules eavaluation.
# finally preparing the output in the desired structure and printing it out
for i in ret.items:
    
    # rule1: ensure the pod only uses images prefixed with 'bitnami/'
    
    prefix_name = i.spec.containers[0].image
    if prefix_name.startswith('bitnami'):
        image_prefix_status = True
    
    # rule2: ensure the pod contains a label 'team' with some value
    
    else:
        image_prefix_status = False
    try:
        labels = i.metadata.labels.app
        labels_value = i.metadata.labels["pod-template-hash"]
        if not labels_value:
         label_status = False
        elif "team" in labels:
            label_status = True
        else:
            label_status = False
    except:
        label_status = False
     
    # rule3: ensure the pod has not been running for more than 7 days according to its strat time
    
    start_time = i.status.container_statuses[0].state.running.started_at
    start_time = datetime(start_time.year, start_time.month, start_time.day, start_time.hour, start_time.minute, start_time.second, 0)
    time_now = datetime.now()
    seven_days_prior = time_now - timedelta(days=7)
    start_time_status =  start_time < seven_days_prior
    
    # final output in the requrested format
    
    output = {"pod":i.metadata.name,
              "rule_evaluation":[{"name":"image_prefix",
                                  "valid":image_prefix_status},
                                  {"name":"team_label_present",
                                   "valid":label_status},
                                  {"name":"recent_start_time",
                                   "valid":start_time_status}
                                  ]
              }
    print(output)
