from stacks.template_path import path
from scripts.stacks import Stack, stack_name


def my_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage=stage, tenant=tenant, name="LoadBalancer")


def stack(
    stage: str,
    tenant: str,
    vpc_id: str,
    subnets: str,
    has_private_subnet: bool,
) -> Stack:
    return Stack(
        template=path("lb", "load_balancers.yaml"),
        stack_name=my_stack_name(stage, tenant),
        parameters={
            "Tenant": stage,
            "Stage": tenant,
            "VpcId": vpc_id,
            "SubnetIdList": subnets,
            "HasPrivateSubnet": "true" if has_private_subnet else "false",
        },
    )
