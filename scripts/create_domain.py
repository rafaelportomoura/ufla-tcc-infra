from stacks import domain
from scripts.cloudformation import CloudFormation
from scripts.exception import DeployException
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
log_level = args["log_level"]
cloudformation = CloudFormation(profile=profile, region=region, log_level=log_level)

################################################
#  🚀 DOMAIN DEPLOY
################################################
DOMAIN_STACK = domain.stack(stage=stage, tenant=tenant, domain_name="rafamoura.com.br")
cloudformation.deploy_stack(DOMAIN_STACK)

if not cloudformation.stack_is_succesfully_deployed(DOMAIN_STACK["stack_name"]):
    raise DeployException(DOMAIN_STACK)
