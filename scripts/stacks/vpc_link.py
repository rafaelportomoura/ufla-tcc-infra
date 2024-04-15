from stacks.template_path import path
from utils.stacks import Stack, stack_name


def stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage, tenant, "VpcLink")


def stack(
    stage: str,
    tenant: str,
    private_subnets: str,
    private_security_groups: str,
) -> Stack:
    return Stack(
        template=path("api", "vpc_link.yaml"),
        stack_name=stack_name(stage, tenant),
        parameters={
            "Tenant": stage,
            "Stage": tenant,
            "Subnets": private_subnets,
            "SecurityGroups": private_security_groups,
        },
    )
