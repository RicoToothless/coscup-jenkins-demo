from aws_cdk import (
    core,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_eks as eks,
)

from env import get_eks_admin_iam_username
from eks_cluster.load_config_files import read_helm_config

class EksClusterStack(core.Stack):

    def __init__(self, scope: core.Construct, name: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        cluster = eks.Cluster(
            self, 'coscup-jenkins-demo-cluster',
            vpc=vpc,
            version=eks.KubernetesVersion.V1_16,
            default_capacity=0
        )

        asg_worker_nodes = cluster.add_capacity(
            'worker-node',
            instance_type=ec2.InstanceType('t3a.large'),
            spot_price='0.0936',
            desired_capacity=2
        )

        asg_jenkins_slave = cluster.add_capacity(
            'worker-node-jenkins-slave',
            instance_type=ec2.InstanceType('t3a.small'),
            spot_price='0.0234',
            desired_capacity=1,
            bootstrap_options=eks.BootstrapOptions(
                kubelet_extra_args='--node-labels jenkins=slave --register-with-taints jenkins=slave:NoSchedule'
            )
        )

        asg_worker_nodes.connections.allow_from(
            asg_jenkins_slave,
            ec2.Port.all_traffic()
        )
        asg_jenkins_slave.connections.allow_from(
            asg_worker_nodes,
            ec2.Port.all_traffic()
        )

        eks_master_role = iam.Role(
            self, 'AdminRole',
            assumed_by=iam.ArnPrincipal(get_eks_admin_iam_username())
        )

        cluster.aws_auth.add_masters_role(eks_master_role)

        stable_chart = 'https://kubernetes-charts.storage.googleapis.com'

        eks.HelmChart(
            self, 'jenkins',
            release='jenkins',
            cluster=cluster,
            repository=stable_chart,
            chart='jenkins',
            namespace='jenkins',
            version='2.3.3',
            values={
                'master': {
                    'tag': '2.235.1', 'adminPassword': 'admin', 'serviceType': 'LoadBalancer',
                    'installPlugins': ['kubernetes:1.26.3', 'git:4.3.0', 'workflow-aggregator:2.6', 'credentials-binding:1.23', 'workflow-job:2.39', 'configuration-as-code:1.42','job-dsl:1.77'],
                    'serviceAnnotations': {
                        'service.beta.kubernetes.io/aws-load-balancer-type': 'nlb'
                    },
                    'JCasC': {'enabled': True,
                        'configScripts': {
                            'settings': read_helm_config('eks_cluster/helm_config/jenkins-jcasc-settings.yaml')
                        }
                    }
                }
            }
        )

        eks.HelmChart(
            self, 'kube-ops-view',
            release='kube-ops-view',
            cluster=cluster,
            repository=stable_chart,
            chart='kube-ops-view',
            namespace='monitor',
            version='1.2.0',
            values={
                'service': {'type': 'LoadBalancer'},
                'rbac': {'create': True}
            }
        )

        eks.HelmChart(
            self, 'dummy-service',
            release='dummy-service',
            cluster=cluster,
            repository=stable_chart,
            chart='kibana',
            namespace='default',
            version='3.2.6',
            values={
                'replicaCount': '60'
            }
        )