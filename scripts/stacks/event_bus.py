from stacks.template_path import path
from utils.stacks import Stack, stack_name


def stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage, tenant, "EventBus")


def stack(
    stage: str,
    tenant: str,
) -> Stack:
    return Stack(
        template=path("sns", "event_bus.yaml"),
        stack_name=stack_name(stage, tenant),
        parameters={
            "Tenant": stage,
            "Stage": tenant,
        },
    )
