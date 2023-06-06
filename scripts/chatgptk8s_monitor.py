#!/usr/bin/python3
import os
import requests
import openai
import json
from kubernetes import client, config
from kubernetes.client import configuration
from kubernetes.stream import stream 

config.load_kube_config()
configuration.assert_hostname = False
k8sapi = client.CoreV1Api()
openai.api_key = os.getenv("OPENAI_API_KEY")

resp_obj = k8sapi.list_pod_for_all_namespaces(
	watch=False,
	_preload_content=False
	)
pods_all = json.loads(resp_obj.data)

## chatgpt func
def chatgptcall(input):
	response = openai.ChatCompletion.create(
		model = "gpt-3.5-turbo",
		messages = [{"role":"user", "content": input}]
	)
	output = response.choices[0].message.content
	return output
	print(output)


for pod in pods_all["items"]:
	pod_name  = pod["metadata"]["name"]
	pod_ns = pod["metadata"]["namespace"] 
	pod_details = json.loads((k8sapi.read_namespaced_pod(name=pod_name, namespace=pod_ns, _preload_content=False)).data)
	for container in pod_details["status"]["containerStatuses"]:
		#print(container)
		if "waiting" in container["state"]:
			try:
				#pod_log = k8sapi.read_namespaced_pod_log(name=pod_name, container=container["name"], namespace=pod_ns, _preload_content=False).data
				#print(pod_log)
				#print(pod_log)
				input = container["state"]["waiting"]["message"]
				print(input)
				out = chatgptcall(input)
				print(out)
			except Exception as e:
				print("error_log: "+ str(e))
				#print("this is error")
			#print(pod_log)
	print("-------")
