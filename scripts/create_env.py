import os
import sys
from typing import Any
from cloudformation import CloudFormation
from log import Log
import stacks

ROOT = os.path.dirname(os.path.dirname(__file__))

stage = sys.argv[1] if len(sys.argv) > 1 else 'dev'
tenant = sys.argv[2] if len(sys.argv) > 2 else 'tcc'
region = sys.argv[3] if len(sys.argv) > 3 else 'us-east-2'
profile = sys.argv[4] if len(sys.argv) > 4 else 'tcc'
log_level = int(sys.argv[5],base=10) if len(sys.argv) > 5 else 3

cloudformation = CloudFormation(profile,region,log_level)
log = Log(log_level)

def deploy_stack(stack: dict[str, Any]) -> None:
    template = os.path.join(ROOT,stack['template'])
    stack_name = stack['stack_name']
    parameters = stack['parameters']
    log.checkpoint(f'Deploy of {stack_name}')
    cloudformation.deploy(template,stack_name,parameters)


################################################
#  🚀 VPC DEPLOY
################################################
VPC_STACK = stacks.vpc(stage, tenant)
deploy_stack(VPC_STACK)

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
public_subnet_a = PUBLIC_SUBNETS_IDS.split(',')[0]
NAT_GATEWAY_STACK = stacks.nat_gateway(stage, tenant,'a',public_subnet_a,PRIVATE_ROUTE_TABLE_ID)
# deploy_stack(NAT_GATEWAY_STACK)

################################################
# 🚀 INTERFACE_ENDPOINTS
################################################
INTERFACE_ENDPOINTS_STACK = stacks.interface_endpoints(stage, tenant,VPC_ID,PRIVATE_SUBNETS_IDS,PRIVATE_SECURITY_GROUP)
# deploy_stack(INTERFACE_ENDPOINTS_STACK)

################################################
# 🚀 VPC_LINK
################################################
VPC_LINK_STACK = stacks.vpc_link(stage, tenant, PRIVATE_SUBNETS_IDS, PRIVATE_SECURITY_GROUP)
# deploy_stack(VPC_LINK_STACK)

################################################
# 🚀 DOMAIN
################################################
DOMAIN_STACK = stacks.domain(stage, tenant)
deploy_stack(DOMAIN_STACK)

exports = cloudformation.list_exports()
DOMAIN_NAME = cloudformation.get_export_value(exports,f"{stage}-{tenant}-domain-name" )
HOSTED_ZONE_ID = cloudformation.get_export_value(exports,f"{stage}-{tenant}-hosted-zone-id" )
CERTIFICATE = cloudformation.get_export_value(exports,f"{stage}-{tenant}-domain-certificate" )

################################################
# 🚀 API GATEWAY
################################################
API_GATEWAY_STACK = stacks.api_gateway(stage, tenant, DOMAIN_NAME, HOSTED_ZONE_ID, CERTIFICATE)
deploy_stack(API_GATEWAY_STACK)

################################################
# 🚀 PACKAGE_BUCKET
################################################
PACKAGE_BUCKET_STACK = stacks.package_bucket()
deploy_stack(PACKAGE_BUCKET_STACK)

################################################
# 🚀 SES
################################################
SES_STACK = stacks.ses(stage,tenant,'',True)
deploy_stack(SES_STACK)

exports = cloudformation.list_exports()
EMAIL_IDENTITY = cloudformation.get_export_value(exports,f"{stage}-{tenant}-email-identity" )
SES = cloudformation.get_export_value(exports,f"{stage}-{tenant}-ses")

################################################
# 🚀 COGNITO
################################################
COGNITO_STACK = stacks.cognito(stage,tenant,EMAIL_IDENTITY)
deploy_stack(COGNITO_STACK)