from stacks.template_path import path
from scripts.stacks import Stack, stack_name


def stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage, tenant, "Vpc-Nat-Gateway")


def stack(
    stage: str,
    tenant: str,
    nat_name: str,
    public_subnet: str,
    private_route_table_id: str,
) -> Stack:
    return Stack(
        template=path("vpc", "nat_gateway.yaml"),
        stack_name=stack_name(stage, tenant),
        parameters={
            "Tenant": stage,
            "Stage": tenant,
            "NatName": nat_name,
            "PublicSubnet": public_subnet,
            "PrivateRouteTableId": private_route_table_id,
        },
    )
