#!/bin/sh

set -e
set -x

export EKS_ADMIN_IAM_USERNAME=`aws sts get-caller-identity | jq '.Arn' | cut -d '"' -s -f2`
echo $EKS_ADMIN_IAM_USERNAME
cdk bootstrap
cdk list
cdk deploy --require-approval never vpc-stack eks-cluster