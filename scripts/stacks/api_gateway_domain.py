from stacks.template_path import path
from scripts.stacks import Stack, stack_name


def my_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage=stage, tenant=tenant, name="ApiGatewayDomain")


def stack(
    stage: str, tenant: str, domain_name: str, hosted_zone: str, certificate: str
) -> Stack:
    return Stack(
        template=path("domain", "certificate.yaml"),
        stack_name=my_stack_name(stage, tenant),
        parameters={
            "Tenant": tenant,
            "Stage": stage,
            "DomainName": domain_name,
            "HostedZone": hosted_zone,
            "Certificate": certificate,
        },
    )
