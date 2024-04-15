from stacks import interface_endpoints, nat_gateway, vpc, vpc_link
from scripts.cloudformation import CloudFormation
from scripts.args import get_args


args = get_args(
    {
        "stage": {"type": "str", "required": False, "default": "prod"},
        "tenant": {"type": "str", "required": False, "default": "tcc"},
        "region": {"type": "str", "required": False, "default": "us-east-2"},
        "profile": {"type": "str", "required": False, "default": "default"},
        "log_level": {"type": "int", "required": False, "default": 3},
    }
)

stage = args["stage"]
tenant = args["tenant"]
region = args["region"]
profile = args["profile"]

cloudformation = CloudFormation(profile, region, log_level=args["log_level"])

################################################
#  🚀 VPC DEPLOY
################################################
VPC_STACK = vpc.stack(stage, tenant)
cloudformation.deploy_stack(VPC_STACK)

exports = cloudformation.list_exports()
VPC_ID = cloudformation.get_export_value(exports, f"{stage}-{tenant}-vpc-id")
PRIVATE_SECURITY_GROUP = cloudformation.get_export_value(
    exports, f"{stage}-{tenant}-private-subnet-security-group-id"
)
PRIVATE_SUBNETS_IDS = cloudformation.get_export_value(
    exports, f"{stage}-{tenant}-private-subnets-list"
)
PUBLIC_SECURITY_GROUP = cloudformation.get_export_value(
    exports, f"{stage}-{tenant}-public-subnet-security-group-id"
)
PUBLIC_SUBNETS_IDS = cloudformation.get_export_value(
    exports, f"{stage}-{tenant}-public-subnets-list"
)
PRIVATE_ROUTE_TABLE_ID = cloudformation.get_export_value(
    exports, f"{stage}-{tenant}-private-route-table-id"
)

################################################
# 🚀 NAT_GATEWAY
################################################
public_subnet_a = PUBLIC_SUBNETS_IDS.split(",")[0] if PUBLIC_SUBNETS_IDS else None
NAT_GATEWAY_STACK = nat_gateway.stack(
    stage, tenant, "a", public_subnet_a, PRIVATE_ROUTE_TABLE_ID
)
cloudformation.deploy_stack(NAT_GATEWAY_STACK)

################################################
# 🚀 INTERFACE_ENDPOINTS
################################################
INTERFACE_ENDPOINTS_STACK = interface_endpoints.stack(
    stage, tenant, VPC_ID, PRIVATE_SUBNETS_IDS, PRIVATE_SECURITY_GROUP
)
cloudformation.deploy_stack(INTERFACE_ENDPOINTS_STACK)

################################################
# 🚀 VPC LINKS
################################################
VPC_LINKS_STACK = vpc_link.stack(
    stage=stage, tenant=tenant, private_security_groups=PRIVATE_SECURITY_GROUP
)
cloudformation.deploy_stack(VPC_LINKS_STACK)
