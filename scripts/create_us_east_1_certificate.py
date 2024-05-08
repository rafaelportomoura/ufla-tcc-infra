from stacks import certificate, api_gateway_domain
from scripts.cloudformation import CloudFormation
from scripts.args import get_args
from scripts.exception import DeployException


args = get_args(
    {
        "stage": {"type": "str", "required": False, "default": "prod"},
        "tenant": {"type": "str", "required": False, "default": "tcc"},
        "profile": {"type": "str", "required": False, "default": "default"},
        "log_level": {"type": "int", "required": False, "default": 3},
    }
)

stage = args["stage"]
tenant = args["tenant"]
region = "us-east-1"
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
print(CERTIFICATE)
if not cloudformation.stack_is_succesfully_deployed(CERTIFICATE_STACK["stack_name"]):
    raise DeployException(CERTIFICATE_STACK)
