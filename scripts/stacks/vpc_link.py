from stacks.template_path import path
from scripts.stacks import Stack, stack_name


def my_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage=stage, tenant=tenant, name="VpcLink")


def stack(
    stage: str,
    tenant: str,
    private_subnets: str,
    private_security_groups: str,
) -> Stack:
    return Stack(
        template=path("api", "vpc_link.yaml"),
        stack_name=my_stack_name(stage, tenant),
        parameters={
            "Tenant": stage,
            "Stage": tenant,
            "Subnets": private_subnets,
            "SecurityGroups": private_security_groups,
        },
    )
