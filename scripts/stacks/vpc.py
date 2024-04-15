from stacks.template_path import path
from utils.stacks import Stack, stack_name


def stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage, tenant, "Vpc")


def stack(stage: str, tenant: str) -> Stack:
    return Stack(
        template=path("vpc", "vpc.yaml"),
        stack_name=stack_name(stage, tenant),
        parameters={
            "Stage": stage,
            "Tenant": tenant,
            "VpcCidr": "10.1.0.0/16",
            "PrivateSubnetACidr": "172.31.0.0/18",
            "PrivateSubnetBCidr": "172.31.64.0/18",
            "PublicSubnetACidr": "172.31.128.0/18",
            "PublicSubnetBCidr": "172.31.192.0/18",
        },
    )


# https://nuvibit.com/vpc-subnet-calculator/
