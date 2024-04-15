from stacks.template_path import path
from scripts.stacks import Stack, stack_name


def my_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage, tenant, "ApiGatewayDomain")


def stack(
    stage: str, tenant: str, domain_name: str, hosted_zone: str, certificate: str
) -> Stack:
    return Stack(
        template=path("domain", "certificate.yaml"),
        stack_name=my_stack_name(stage, tenant),
        parameters={
            "Tenant": stage,
            "Stage": tenant,
            "DomainName": domain_name,
            "HostedZone": hosted_zone,
            "Certificate": certificate,
        },
    )
