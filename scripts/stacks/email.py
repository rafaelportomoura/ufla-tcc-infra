from stacks.template_path import path
from scripts.stacks import Stack, stack_name


def my_stack_name() -> str:
    return "EmailIdentityStack-Deploy"


def stack(
    email: str,
) -> Stack:
    return Stack(
        template=path("ses", "email_identity.yaml"),
        stack_name=my_stack_name(),
        parameters={
            "Email": email,
        },
    )
