#!/bin/sh

jenkins_ep=$(kubectl get svc jenkins -n jenkins -o jsonpath="{.status.loadBalancer.ingress[0].hostname}")

echo "jenkins"
echo "http://${jenkins_ep}:8080"

kube_ops_view_ep=$(kubectl get svc kube-ops-view -n monitor -o jsonpath="{.status.loadBalancer.ingress[0].hostname}")

echo "kube-ops-view"
echo "http://${kube_ops_view_ep}"