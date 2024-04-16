from stacks.template_path import path
from scripts.stacks import Stack, stack_name


def my_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage=stage, tenant=tenant, name="Certificate")


def stack(stage: str, tenant: str, hosted_zone: str) -> Stack:
    return Stack(
        template=path("domain", "certificate.yaml"),
        stack_name=my_stack_name(stage, tenant),
        parameters={
            "Tenant": tenant,
            "Stage": stage,
            "HostedZone": hosted_zone,
        },
    )
