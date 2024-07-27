import os
import json
import uuid
import traceback
from software_composition_analysis.core.logger import logger
from software_composition_analysis.core.models import Response
from software_composition_analysis.support.enums import (
    STDInput,
    MixedTypeEnum,
    ResponseMessage,
)


def run(
    target: str,
    target_type: str,
) -> Response:
    resp = Response()
    data = None
    file = os.path.join(
        os.path.join(
            os.getcwd(),
            MixedTypeEnum.TMP.value,
        ),
        str(f"{uuid.uuid4()}.json"),
    )
    try:
        os.system(
            STDInput.TRIVY.value.format(
                target_type=target_type,
                target=target,
                output=file,
            )
        )
        with open(file, "r") as fp:
            data = json.load(fp, strict=False)
        if data:
            resp.success = MixedTypeEnum.SUCCESS.value
            resp.data = data
    except Exception as err:
        resp.message = ResponseMessage.TRIVY_MSG.value
        logger.error(err)
        logger.debug(traceback.format_exc())

    return resp
