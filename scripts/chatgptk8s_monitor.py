#!/usr/bin/python3
import requests
import json
from kubernetes import client, config

config.load_kube_config()

v1 = client.CoreV1Api()

resp_obj = v1.list_pod_for_all_namespaces(
	watch=False,
	_preload_content=False
	)
pods_all = json.loads(resp_obj.data)


for pod in pods_all["items"]:
	print(pod["metadata"]["name"])
