import os
from typing import Any

def stack_name(stage: str, tenant: str, name: str) -> str:
    return f'{stage[0].upper() + stage[1:]}-{tenant[0].upper() + tenant[1:]}-{name}-Deploy'

def vpc_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage,tenant,'Vpc')
def vpc(stage: str, tenant: str) -> dict[str, Any]:
    return {
        'template': os.path.join('network','vpc.yaml'),
        'stack_name': vpc_stack_name(stage,tenant),
        'parameters': {
            'Stage': stage,
            'Tenant': tenant,
            'VpcCidr': '10.1.0.0/16',
            'PrivateSubnetACidr': '10.1.1.0/24',
            'PrivateSubnetBCidr': '10.1.2.0/24',
            'PublicSubnetACidr': '10.1.3.0/24',
            'PublicSubnetBCidr': '10.1.4.0/24',
        }
    }

def domain_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage,tenant,'Domain-Name')
def domain(stage: str, tenant: str, domain = 'rafamoura.com.br') -> dict[str, Any]:
    return {
        'template': os.path.join('network','domain.yaml'),
        'stack_name': domain_stack_name(stage,tenant),
        'parameters': {
            'Stage': stage,
            'Tenant': tenant,
            'DomainName': domain
        }
    }

def api_gateway_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage,tenant,'Api-Gateway')
def api_gateway(stage: str, tenant: str, domain_name: str, hosted_zone: str, certificate: str) -> dict[str, Any]:
    return {
        'template': os.path.join('network','api_gateway_domain.yaml'),
        'stack_name': api_gateway_stack_name(stage,tenant),
        'parameters': {
            'Stage': stage,
            'Tenant': tenant,
            'DomainName': domain_name,
            'HostedZone': hosted_zone,
            'Certificate': certificate,
        },
    }

def vpc_link_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage,tenant,'Api-Gateway-Vpc-Link')
def vpc_link(stage: str, tenant: str, subnets: list[str], security_groups: list[str]) -> dict[str, Any]:
    return {
        'template': os.path.join('network','vpc_link.yaml'),
        'stack_name': vpc_link_stack_name(stage,tenant),
        'parameters': {
            'Stage': stage,
            'Tenant': tenant,
            'Subnets': subnets,
            'SecurityGroups': security_groups,
        },
    }

def interface_endpoints_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage,tenant,'Vpc-Interface-Endpoints')
def interface_endpoints(stage: str, tenant: str, vpc_id: str, subnets: list[str], security_groups: list[str]) -> dict[str, Any]:
    return {
        'template': os.path.join('network','interface_endpoints.yaml'),
        'stack_name': interface_endpoints_stack_name(stage,tenant),
        'parameters': {
            'Stage': stage,
            'Tenant': tenant,
            'VpcId': vpc_id,
            'SubnetIdsList': subnets,
            'SecurityGroupIdList': security_groups,
        },
    }

def nat_gateway_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage,tenant,'Vpc-Nat-Gateway')
def nat_gateway(stage: str, tenant: str, nat_name: str, public_subnet: str, private_route_table_id: str) -> dict[str, Any]:
    return {
        'template': os.path.join('network','nat_gateway.yaml'),
        'stack_name': nat_gateway_stack_name(stage,tenant),
        'parameters': {
            'Tenant': stage,
            'Stage': tenant,
            'NatName': nat_name,
            'PublicSubnet': public_subnet,
            'PrivateRouteTableId': private_route_table_id,
        },
    }

def ses_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage,tenant,'Ses')
def ses(stage: str, tenant: str, email: str, feedback = False ) -> dict[str, Any]:
    return {
        'template': os.path.join('ses','ses.yaml'),
        'stack_name': ses_stack_name(stage,tenant),
        'parameters': {
            'Stage': stage,
            'Tenant': tenant,
            'EmailIdentityParam': email,
            'EmailFeedback': 'true' if feedback else 'false' ,
        },
    }

def package_bucket_stack_name() -> str:
    return 'Package-Bucket-Deploy'
def package_bucket() -> dict[str, Any]:
    return {
        'template': os.path.join('s3','package_bucket.yaml'),
        'stack_name': package_bucket_stack_name(),
        'parameters': None
    }

def cognito_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage,tenant,'Cognito')
def cognito(stage: str, tenant: str, email_identity: str) -> dict[str, Any]:
    return {
        'template': os.path.join('cognito','user_pool.yaml'),
        'stack_name': cognito_stack_name(stage,tenant),
        'parameters': {
            'Stage': stage,
            'Tenant': tenant,
            'EmailIdentity': email_identity,
        }
    }

def event_bus_stack_name(stage: str, tenant: str) -> str:
    return stack_name(stage,tenant,'Cognito')
def event_bus(stage: str, tenant: str) -> dict[str, Any]:
    return {
        'template': os.path.join('sns','event_bus.yaml'),
        'stack_name': cognito_stack_name(stage,tenant),
        'parameters': {
            'Stage': stage,
            'Tenant': tenant
        }
    }