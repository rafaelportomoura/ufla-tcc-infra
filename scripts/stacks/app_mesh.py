from stacks.template_path import path
from scripts.stacks import Stack, stack_name


def my_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage=stage, tenant=tenant, name="AppMesh")


def stack(
    stage: str,
    tenant: str,
) -> Stack:
    return Stack(
        template=path("app_mesh", "app_mesh.yaml"),
        stack_name=my_stack_name(stage, tenant),
        parameters={
            "Tenant": tenant,
            "Stage": stage,
        },
    )
