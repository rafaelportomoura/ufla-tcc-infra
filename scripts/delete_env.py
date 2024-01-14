import os
import sys
from typing import Any
from utils.cloudformation import CloudFormation
from utils.log import Log
import utils.stacks as stacks

ROOT = os.path.dirname(os.path.dirname(__file__))

stage = sys.argv[1] if len(sys.argv) > 1 else 'dev'
tenant = sys.argv[2] if len(sys.argv) > 2 else 'tcc'
region = sys.argv[3] if len(sys.argv) > 3 else 'us-east-2'
profile = sys.argv[4] if len(sys.argv) > 4 else 'tcc'
log_level = int(sys.argv[5],base=10) if len(sys.argv) > 5 else 3

cloudformation = CloudFormation(profile,region,log_level)
log = Log(log_level)


def remove_from_bucket(bucket: str) -> None:
    cmd = f"aws --profile {profile} s3 rm s3://{bucket} --recursive"
    log.cmd(cmd)
    os.system(cmd)

cloudformation.delete_stack(stacks.event_bus_stack_name(stage,tenant))
cloudformation.delete_stack(stacks.cognito_stack_name(stage,tenant))
cloudformation.delete_stack(stacks.ses_stack_name(stage,tenant))
cloudformation.delete_stack(stacks.api_gateway_stack_name(stage,tenant))
remove_from_bucket(f"package-bucket-{region}")
cloudformation.delete_stack(stacks.package_bucket_stack_name())
cloudformation.delete_stack(stacks.certificate_stack_name(stage,tenant))
cloudformation.delete_stack(stacks.domain_stack_name(stage,tenant))
cloudformation.delete_stack(stacks.interface_endpoints_stack_name(stage,tenant))
cloudformation.delete_stack(stacks.nat_gateway_stack_name(stage,tenant))
cloudformation.delete_stack(stacks.vpc_link_stack_name(stage,tenant))
cloudformation.delete_stack(stacks.vpc_stack_name(stage,tenant))