#!/bin/sh

# get aws eks kube-config

EKS_CLUSTER_NAME=`aws eks list-clusters | grep coscupjenkinsdemocluster | cut -d '"' -s -f2`
EKS_ADMIN_ARN=`aws iam list-roles | grep eks-cluster-AdminRole | grep Arn | cut -d'"' -s -f4`
EKS_CLUSTER_ARN=`aws eks describe-cluster --name $EKS_CLUSTER_NAME | jq '.cluster.arn' | cut -d '"' -s -f2`

aws eks update-kubeconfig --region ap-northeast-2 --name $EKS_CLUSTER_NAME --role-arn $EKS_ADMIN_ARN

kubectl config use-context $EKS_CLUSTER_ARN