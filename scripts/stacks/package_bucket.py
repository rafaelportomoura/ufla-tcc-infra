from stacks.template_path import path
from scripts.stacks import Stack, stack_name


def my_stack_name() -> str:
    return stack_name(name="PackageBucket")


def stack() -> Stack:
    return Stack(template=path("s3", "package_bucket.yaml"), stack_name=my_stack_name())
