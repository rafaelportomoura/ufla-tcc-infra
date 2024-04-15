from scripts.stacks import domain
from scripts.utils.cloudformation import CloudFormation
from scripts.utils.args import get_args


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

################################################
#  🚀 DOMAIN DEPLOY
################################################
DOMAIN_STACK = domain.stack(stage=stage, tenant=tenant, domain_name="rafamoura.com.br")
cloudformation.deploy_stack(DOMAIN_STACK)

exports = cloudformation.list_exports()
HOSTED_ZONE_ID = cloudformation.get_export_value(
    exports, f"{stage}-{tenant}-hosted-zone-id"
)
