import os
import sys
from typing import Any
from cloudformation import CloudFormation
from log import Log
import stacks

ROOT = os.path.dirname(os.path.dirname(__file__))

stage = sys.argv[1] if len(sys.argv) > 1 else 'dev'
tenant = sys.argv[2] if len(sys.argv) > 2 else 'tcc'
region = sys.argv[3] if len(sys.argv) > 3 else 'us-east-2'
profile = sys.argv[4] if len(sys.argv) > 4 else 'tcc'
log_level = int(sys.argv[5],base=10) if len(sys.argv) > 5 else 3

cloudformation = CloudFormation(profile,region,log_level)
log = Log(log_level)

def delete(stack_name: str) -> None:
    log.checkpoint(f'Deleting {stack_name}')    
    cloudformation.delete_stack(stack_name)

def remove_from_bucket(bucket: str) -> None:
    cmd = f"aws --profile {profile} s3 rm s3://{bucket} --recursive"
    log.cmd(cmd)
    os.system(cmd)

delete(stacks.event_bus_stack_name(stage,tenant))
delete(stacks.cognito_stack_name(stage,tenant))
delete(stacks.ses_stack_name(stage,tenant))
delete(stacks.api_gateway_stack_name(stage,tenant))
remove_from_bucket(f"package-bucket-{region}")
delete(stacks.package_bucket_stack_name())
delete(stacks.certificate_stack_name(stage,tenant))
delete(stacks.domain_stack_name(stage,tenant))
delete(stacks.interface_endpoints_stack_name(stage,tenant))
delete(stacks.nat_gateway_stack_name(stage,tenant))
delete(stacks.vpc_link_stack_name(stage,tenant))
delete(stacks.vpc_stack_name(stage,tenant))