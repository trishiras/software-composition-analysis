import os
import json
from argparse import Namespace
from software_composition_analysis.services import trivy
from software_composition_analysis.core.logger import logger
from software_composition_analysis.core.input import parse_args
from software_composition_analysis.support.enums import MixedTypeEnum


class SoftwareCompositionAnalysis(object):
    def __init__(
        self,
        arguments: Namespace,
    ):
        self.data = {}
        self.target = arguments.target
        self.target_type = arguments.target_type
        self.output_via = arguments.output_via
        self.webhook = arguments.webhook
        self.output_file_path = arguments.output_file_path

    def run(self):

        logger.info(
            f"Started generating software composition analysis for target :- {self.target}"
        )

        if self.webhook:
            logger.info(f"Webhook URL :- {self.webhook}")

        if self.output_file_path:
            logger.info(f"Output file path :- {self.output_file_path}")

        output_dir = os.path.join(
            os.getcwd(),
            MixedTypeEnum.OUTPUT.value,
        )
        tmp_dir = os.path.join(
            os.getcwd(),
            MixedTypeEnum.TMP.value,
        )
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)

        trivy_response = trivy.run(
            target=self.target,
            target_type=self.target_type,
        )

        if trivy_response.success:
            self.data = trivy_response.data
        else:
            logger.error(trivy_response.message)

        with open(self.output_file_path, "w") as fp:
            json.dump(self.data, fp, indent=4, default=str)

        logger.info(
            f"Finished generating software composition analysis for target :- {self.target}"
        )


def main():

    arguments, unknown = parse_args()

    software_bill_of_materials = SoftwareCompositionAnalysis(arguments=arguments)
    software_bill_of_materials.run()
