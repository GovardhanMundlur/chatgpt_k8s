#!/usr/bin/python3
import requests
import json
from kubernetes import client, config
from kubernetes.client import configuration 

config.load_kube_config()
configuration.assert_hostname = False
k8sapi = client.CoreV1Api()

resp_obj = k8sapi.list_pod_for_all_namespaces(
	watch=False,
	_preload_content=False
	)
pods_all = json.loads(resp_obj.data)


for pod in pods_all["items"]:
	pod_name  = pod["metadata"]["name"]
	pod_ns = pod["metadata"]["namespace"] 
	pod_details = json.loads((k8sapi.read_namespaced_pod(name=pod_name, namespace=pod_ns, _preload_content=False)).data)
	for container in pod_details["status"]["containerStatuses"]:
		if "waiting" in container["state"]:
			pod_log = json.loads((k8sapi.read_namespaced_pod_log(name=pod_name, namespace=pod_ns, _preload_content=False)).data)
			#print(pod_log)
	print("-------")
