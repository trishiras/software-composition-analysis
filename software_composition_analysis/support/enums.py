from enum import Enum


class MixedTypeEnum(Enum):
    # Boolean constants
    SUCCESS = True

    # String constants
    OUTPUT = "output"
    TMP = "tmp"


class ResponseMessage(Enum):
    TRIVY_MSG = "TRIVY did not return any response"


class STDInput(Enum):
    TRIVY = (
        "trivy {target_type} {target} --scanners vuln --format json --output {output}"
    )
