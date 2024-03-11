from utils.stacks import Stack, stack_name
from stacks.template_path import path


def stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage, tenant, "Vpc-Interface-Endpoints")


def stack(
    stage: str, tenant: str, vpc_id: str, subnets: list[str], security_groups: list[str]
) -> Stack:
    Stack(
        template=path("vpc", "interface_endpoints.yaml"),
        stack_name=stack_name(stage, tenant),
        parameters={
            "Stage": stage,
            "Tenant": tenant,
            "VpcId": vpc_id,
            "SubnetIdsList": subnets,
            "SecurityGroupIdList": security_groups,
        },
    )
