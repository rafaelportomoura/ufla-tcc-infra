from stacks.template_path import path
from scripts.stacks import Stack, stack_name


def stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage, tenant, "Domain")


def stack(stage: str, tenant: str, domain_name: str) -> Stack:
    return Stack(
        template=path("domain", "domain.yaml"),
        stack_name=stack_name(stage, tenant),
        parameters={
            "Tenant": stage,
            "Stage": tenant,
            "DomainName": domain_name,
        },
    )
