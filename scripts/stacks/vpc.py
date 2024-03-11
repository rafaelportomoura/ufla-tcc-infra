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
            "PrivateSubnetACidr": "10.1.1.0/24",
            "PrivateSubnetBCidr": "10.1.2.0/24",
            "PublicSubnetACidr": "10.1.3.0/24",
            "PublicSubnetBCidr": "10.1.4.0/24",
        },
    )
