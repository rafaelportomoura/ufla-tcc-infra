from stacks import email
from scripts.exception import DeployException
from scripts.cloudformation import CloudFormation
from scripts.args import get_args


args = get_args(
    {
        "region": {"type": "str", "required": False, "default": "us-east-2"},
        "profile": {"type": "str", "required": False, "default": "default"},
        "log_level": {"type": "int", "required": False, "default": 3},
        "email": {"type": "str", "required": True},
    }
)

region = args["region"]
profile = args["profile"]
log_level = args["log_level"]
cloudformation = CloudFormation(profile=profile, region=region, log_level=log_level)

################################################
# 🚀 EMAIL
################################################
EMAIL_STACK = email.stack(email=args["email"])
cloudformation.deploy_stack(EMAIL_STACK)
if not cloudformation.stack_is_succesfully_deployed(EMAIL_STACK["stack_name"]):
    raise DeployException(EMAIL_STACK)
