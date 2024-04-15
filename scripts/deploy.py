import os
from scripts.args import get_args


args = get_args(
    {
        "python": {"type": "str", "required": False, "default": "python3"},
        "stage": {"type": "str", "required": False, "default": "prod"},
        "tenant": {"type": "str", "required": False, "default": "tcc"},
        "region": {"type": "str", "required": False, "default": "us-east-2"},
        "profile": {"type": "str", "required": False, "default": "default"},
        "log_level": {"type": "int", "required": False, "default": 3},
    }
)
python_exec = args["python"]
log_level = args["log_level"]
stage = args["stage"]
tenant = args["tenant"]
region = args["region"]
profile = args["profile"]

dirname = os.path.dirname(__file__)

args = f"stage={stage} tenant={tenant} region={region} profile={profile} log_level={log_level}"

os.system(f"{python_exec} {dirname}/create_vpc.py {args}")
os.system(f"{python_exec} {dirname}/create_network.py {args}")
os.system(f"{python_exec} {dirname}/create_domain.py {args}")
