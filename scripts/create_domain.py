import sys
from utils.cloudformation import CloudFormation
from utils.log import Log
import utils.stacks as stacks


stage = sys.argv[1] if len(sys.argv) > 1 else 'dev'
tenant = sys.argv[2] if len(sys.argv) > 2 else 'tcc'
region = sys.argv[3] if len(sys.argv) > 3 else 'us-east-2'
profile = sys.argv[4] if len(sys.argv) > 4 else 'tcc'
log_level = int(sys.argv[5],base=10) if len(sys.argv) > 5 else 3

cloudformation = CloudFormation(profile,region,log_level)

################################################
# 🚀 DOMAIN
################################################
DOMAIN_STACK = stacks.domain(stage, tenant)
cloudformation.deploy_stack(DOMAIN_STACK)

exports = cloudformation.list_exports()
DOMAIN_NAME = cloudformation.get_export_value(exports,f"{stage}-{tenant}-domain-name" )
HOSTED_ZONE_ID = cloudformation.get_export_value(exports,f"{stage}-{tenant}-hosted-zone-id" )

################################################
# 🚀 CERTIFICATE
################################################
CERTIFICATE_STACK = stacks.certificate(stage, tenant, DOMAIN_NAME, HOSTED_ZONE_ID)
cloudformation.deploy_stack(CERTIFICATE_STACK)