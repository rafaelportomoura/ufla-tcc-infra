from stacks.template_path import path
from scripts.stacks import Stack, stack_name


def my_stack_name(email: str) -> str:
    return email


def stack(
    email: str,
) -> Stack:
    return Stack(
        template=path("ses", "email_identity.yaml"),
        stack_name=my_stack_name(email=email),
        parameters={
            "Email": email,
        },
    )
