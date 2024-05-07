from stacks import document_db
from scripts.exception import DeployException
from scripts.cloudformation import CloudFormation
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
exports = cloudformation.list_exports()
PRIVATE_SUBNETS_IDS = cloudformation.get_export_value(
    exports, f"{stage}-{tenant}-private-subnets-list"
)
PRIVATE_SECURITY_GROUPS = cloudformation.get_export_value(
    exports, f"{stage}-{tenant}-private-subnet-security-group-id"
)
################################################
#  🚀 DCOUMENT DB DEPLOY
################################################
DOCUMENT_DB = document_db.stack(
    stage=stage,
    tenant=tenant,
    subnet_ids_list=PRIVATE_SUBNETS_IDS,
    security_group_id_list=PRIVATE_SECURITY_GROUPS,
)
cloudformation.deploy_stack(DOCUMENT_DB)

if not cloudformation.stack_is_succesfully_deployed(DOCUMENT_DB["stack_name"]):
    raise DeployException(DOCUMENT_DB)
