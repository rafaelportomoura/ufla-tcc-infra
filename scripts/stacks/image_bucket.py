from stacks.template_path import path
from scripts.stacks import Stack, stack_name


def my_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage=stage, tenant=tenant, name="Images-Bucket")


def stack(
    stage: str,
    tenant: str,
    hosted_zone_id: str,
    domain_name: str,
    certificate_arn: str,
) -> Stack:
    return Stack(
        template=path("s3", "image_bucket.yaml"),
        stack_name=my_stack_name(stage, tenant),
        parameters={
            "Stage": stage,
            "Tenant": tenant,
            "HostedZoneId": hosted_zone_id,
            "DomainName": domain_name,
            "CertificateArn": certificate_arn,
        },
    )
