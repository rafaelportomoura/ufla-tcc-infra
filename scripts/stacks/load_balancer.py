from stacks.template_path import path
from utils.stacks import Stack, stack_name


def stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage, tenant, "LoadBalancer")


def stack(
    stage: str,
    tenant: str,
    vpc_id: str,
    subnets: str,
    has_private_subnet: bool,
) -> Stack:
    return Stack(
        template=path("lb", "load_balancers.yaml"),
        stack_name=stack_name(stage, tenant),
        parameters={
            "Tenant": stage,
            "Stage": tenant,
            "VpcId": vpc_id,
            "SubnetIdList": subnets,
            "HasPrivateSubnet": "true" if has_private_subnet else "false",
        },
    )
