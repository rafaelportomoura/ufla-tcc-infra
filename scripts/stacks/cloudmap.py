from stacks.template_path import path
from scripts.stacks import Stack, stack_name


def stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage, tenant, "CloudMap")


def stack(
    stage: str,
    tenant: str,
    vpc_id: str,
) -> Stack:
    return Stack(
        template=path("app_mesh", "cloudmap.yaml"),
        stack_name=stack_name(stage, tenant),
        parameters={
            "Tenant": stage,
            "Stage": tenant,
            "VpcId": vpc_id,
        },
    )
