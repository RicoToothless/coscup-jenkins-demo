#!/usr/bin/env python3

from aws_cdk import core

from vpc.vpc_stack import VpcStack
from eks_cluster.eks_cluster_stack import EksClusterStack
from env import aws_account

app = core.App()

# VPC

vpc_stack = VpcStack(app, 'vpc-stack', env=aws_account)

# EKS

eks_cluster_stack = EksClusterStack(app, "eks-cluster", vpc=vpc_stack.eks_vpc, env=aws_account)

eks_cluster_stack.add_dependency(vpc_stack)

app.synth()