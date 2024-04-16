from stacks import package_bucket
from scripts.cloudformation import CloudFormation
from scripts.args import get_args
from scripts.exception import DeployException


args = get_args(
    {
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
# 🚀 PACKAGE BUCKET
################################################
PACKAGE_BUCKET_STACK = package_bucket.stack()
cloudformation.deploy_stack(PACKAGE_BUCKET_STACK)
if not cloudformation.stack_is_succesfully_deployed(PACKAGE_BUCKET_STACK["stack_name"]):
    raise DeployException(PACKAGE_BUCKET_STACK)
