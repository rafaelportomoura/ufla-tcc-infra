from scripts.cloudformation import CloudFormation
from scripts.args import get_args
from stacks import image_bucket
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

CERTIFICATE_ARN = (
    cloudformation.get_export_value(exports, f"{stage}-{tenant}-domain-certificate")
    if region == "us-east-1"
    else None
)
if region != "us-east-1":
    us_east_1_cloudformation = CloudFormation(
        profile=profile, region="us-east-1", log_level=log_level
    )
    exports = us_east_1_cloudformation.list_exports()
    CERTIFICATE_ARN = us_east_1_cloudformation.get_export_value(
        exports, f"{stage}-{tenant}-domain-certificate"
    )

################################################
# 🚀 IMAGES
################################################
IMAGES_STACK = image_bucket.stack(
    stage=stage,
    tenant=tenant,
    hosted_zone_id=HOSTED_ZONE_ID,
    domain_name=DOMAIN_NAME,
    certificate_arn=CERTIFICATE_ARN,
)
cloudformation.deploy_stack(stack=IMAGES_STACK)
if not cloudformation.stack_is_succesfully_deployed(
    stack_name=IMAGES_STACK["stack_name"]
):
    raise DeployException(stack=IMAGES_STACK)
