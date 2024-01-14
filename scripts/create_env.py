import sys
from utils.cloudformation import CloudFormation
import utils.stacks as stacks


stage = sys.argv[1] if len(sys.argv) > 1 else 'dev'
tenant = sys.argv[2] if len(sys.argv) > 2 else 'tcc'
region = sys.argv[3] if len(sys.argv) > 3 else 'us-east-2'
profile = sys.argv[4] if len(sys.argv) > 4 else 'tcc'
email = sys.argv[5] if len(sys.argv) > 5 else ''
private_subnet_resources = sys.argv[6] == 'true' if len(sys.argv) > 6 else False
log_level = int(sys.argv[7],base=10) if len(sys.argv) > 7 else 3

cloudformation = CloudFormation(profile,region,log_level)


################################################
#  🚀 VPC DEPLOY
################################################
VPC_STACK = stacks.vpc(stage, tenant)
cloudformation.deploy_stack(VPC_STACK)

exports = cloudformation.list_exports()
VPC_ID = cloudformation.get_export_value(exports,f"{stage}-{tenant}-vpc-id" )
PRIVATE_SECURITY_GROUP = cloudformation.get_export_value(exports,f"{stage}-{tenant}-private-subnet-security-group-id" )
PRIVATE_SUBNETS_IDS = cloudformation.get_export_value(exports,f"{stage}-{tenant}-private-subnets-list")
PUBLIC_SECURITY_GROUP = cloudformation.get_export_value(exports,f"{stage}-{tenant}-public-subnet-security-group-id" )
PUBLIC_SUBNETS_IDS = cloudformation.get_export_value(exports,f"{stage}-{tenant}-public-subnets-list")
PRIVATE_ROUTE_TABLE_ID = cloudformation.get_export_value(exports,f"{stage}-{tenant}-private-route-table-id")

################################################
# 🚀 NAT_GATEWAY
################################################
public_subnet_a = PUBLIC_SUBNETS_IDS.split(',')[0] if PUBLIC_SUBNETS_IDS else None
NAT_GATEWAY_STACK = stacks.nat_gateway(stage, tenant,'a',public_subnet_a,PRIVATE_ROUTE_TABLE_ID)
if private_subnet_resources: cloudformation.deploy_stack(NAT_GATEWAY_STACK)

################################################
# 🚀 INTERFACE_ENDPOINTS
################################################
INTERFACE_ENDPOINTS_STACK = stacks.interface_endpoints(stage, tenant,VPC_ID,PRIVATE_SUBNETS_IDS,PRIVATE_SECURITY_GROUP)
if private_subnet_resources: cloudformation.deploy_stack(INTERFACE_ENDPOINTS_STACK)

################################################
# 🚀 VPC_LINK
################################################
VPC_LINK_STACK = stacks.vpc_link(stage, tenant, PRIVATE_SUBNETS_IDS, PRIVATE_SECURITY_GROUP)
if private_subnet_resources: cloudformation.deploy_stack(VPC_LINK_STACK)


################################################
# 🚀 API GATEWAY
################################################
DOMAIN_NAME = cloudformation.get_export_value(exports,f"{stage}-{tenant}-domain-name" )
HOSTED_ZONE_ID = cloudformation.get_export_value(exports,f"{stage}-{tenant}-hosted-zone-id" )
CERTIFICATE = cloudformation.get_export_value(exports,f"{stage}-{tenant}-domain-certificate" )

API_GATEWAY_STACK = stacks.api_gateway(stage, tenant, DOMAIN_NAME, HOSTED_ZONE_ID, CERTIFICATE)
cloudformation.deploy_stack(API_GATEWAY_STACK)

################################################
# 🚀 PACKAGE_BUCKET
################################################
PACKAGE_BUCKET_STACK = stacks.package_bucket()
cloudformation.deploy_stack(PACKAGE_BUCKET_STACK)

################################################
# 🚀 SES
################################################
SES_STACK = stacks.ses(stage,tenant,email,True)
if email != '': cloudformation.deploy_stack(SES_STACK)

exports = cloudformation.list_exports()
EMAIL_IDENTITY = cloudformation.get_export_value(exports,f"{stage}-{tenant}-email-identity" )
SES = cloudformation.get_export_value(exports,f"{stage}-{tenant}-ses")

################################################
# 🚀 COGNITO
################################################
COGNITO_STACK = stacks.cognito(stage,tenant,EMAIL_IDENTITY)
cloudformation.deploy_stack(COGNITO_STACK)

################################################
# 🚀 EVENT_BUS
################################################
EVENT_BUS_STACK = stacks.event_bus(stage,tenant)
cloudformation.deploy_stack(EVENT_BUS_STACK)