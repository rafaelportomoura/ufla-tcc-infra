from stacks.template_path import path
from scripts.stacks import Stack, stack_name


def my_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage=stage, tenant=tenant, name="DocumentDb")


def stack(
    stage: str, tenant: str, subnet_ids_list: str, security_group_id_list: str
) -> Stack:
    return Stack(
        template=path("database", "documentdb.yaml"),
        stack_name=my_stack_name(stage, tenant),
        parameters={
            "Stage": stage,
            "Tenant": tenant,
            "SubnetIdsList": subnet_ids_list,
            "SecurityGroupIdList": security_group_id_list,
        },
    )
