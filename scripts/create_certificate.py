from stacks import certificate, api_gateway_domain
from scripts.cloudformation import CloudFormation
from scripts.args import get_args
from scripts.exception import DeployException


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
log_level = args["log_level"]
cloudformation = CloudFormation(profile=profile, region=region, log_level=log_level)

exports = cloudformation.list_exports()
HOSTED_ZONE_ID = cloudformation.get_export_value(
    exports, f"{stage}-{tenant}-hosted-zone-id"
)
DOMAIN_NAME = cloudformation.get_export_value(exports, f"{stage}-{tenant}-domain-name")
################################################
# 🚀 CERTIFICATE
################################################
CERTIFICATE_STACK = certificate.stack(
    stage=stage, tenant=tenant, hosted_zone=HOSTED_ZONE_ID, domain_name=DOMAIN_NAME
)
cloudformation.deploy_stack(CERTIFICATE_STACK)
exports = cloudformation.list_exports()
CERTIFICATE = cloudformation.get_export_value(
    exports, f"{stage}-{tenant}-domain-certificate"
)

if not cloudformation.stack_is_succesfully_deployed(CERTIFICATE["stack_name"]):
    raise DeployException(CERTIFICATE)
################################################
# 🚀 API GATEWAY DOMAIN
################################################
API_GATEWAY_DOMAIN_STACK = api_gateway_domain.stack(
    stage=stage,
    tenant=tenant,
    domain_name=DOMAIN_NAME,
    hosted_zone=HOSTED_ZONE_ID,
    certificate=CERTIFICATE,
)
cloudformation.deploy_stack(API_GATEWAY_DOMAIN_STACK)

if not cloudformation.stack_is_succesfully_deployed(
    API_GATEWAY_DOMAIN_STACK["stack_name"]
):
    raise DeployException(API_GATEWAY_DOMAIN_STACK)
