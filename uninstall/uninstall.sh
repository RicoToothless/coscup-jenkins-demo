#!/bin/sh

set -x

export EKS_ADMIN_IAM_USERNAME=`aws sts get-caller-identity | jq '.Arn' | cut -d '"' -s -f2`

cd ../01-install-eks-cluster
cdk destroy -f vpc-stack eks-cluster
cd ../uninstall