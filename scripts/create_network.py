from stacks import load_balancer, app_mesh, cloudmap, event_bus
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
VPC_ID = cloudformation.get_export_value(exports, f"{stage}-{tenant}-vpc-id")
PRIVATE_SUBNETS_IDS = cloudformation.get_export_value(
    exports, f"{stage}-{tenant}-private-subnets-list"
)
################################################
#  🚀 LOADBALANCER DEPLOY
################################################
LB_STACK = load_balancer.stack(
    stage=stage,
    tenant=tenant,
    vpc_id=VPC_ID,
    subnets=PRIVATE_SUBNETS_IDS,
    has_private_subnet=True,
)
cloudformation.deploy_stack(LB_STACK)

if not cloudformation.stack_is_succesfully_deployed(LB_STACK["stack_name"]):
    exit(1)
################################################
# 🚀 APP_MESH
################################################
APP_MESH_STACK = app_mesh.stack(stage=stage, tenant=tenant)
cloudformation.deploy_stack(APP_MESH_STACK)
if not cloudformation.stack_is_succesfully_deployed(APP_MESH_STACK["stack_name"]):
    exit(1)

################################################
# 🚀 CLOUDMAP
################################################
CLOUDMAP_STACK = cloudmap.stack(stage=stage, tenant=tenant, vpc_id=VPC_ID)
cloudformation.deploy_stack(CLOUDMAP_STACK)
if not cloudformation.stack_is_succesfully_deployed(CLOUDMAP_STACK["stack_name"]):
    exit(1)

################################################
# 🚀 EVENT BUS
################################################
EVENT_BUS = event_bus.stack(stage=stage, tenant=tenant)
cloudformation.deploy_stack(EVENT_BUS)
if not cloudformation.stack_is_succesfully_deployed(EVENT_BUS["stack_name"]):
    exit(1)
