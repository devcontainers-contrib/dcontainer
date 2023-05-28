from typing import Optional
import os
import glob
from easyfs import Directory

from dcontainer.devcontainer.feature_generation.dir_models.src_dir import SrcDir
from dcontainer.devcontainer.feature_generation.dir_models.test_dir import TestDir
from dcontainer.devcontainer.models.devcontainer_feature_definition import (
    FeatureDefinition,
)


class OCIFeatureGenerator:
    @staticmethod
    def generate(
        feature_definition: str,
        output_dir: str,
        nanolayer_version: Optional[str] = None,
    ) -> None:
        definition_model = FeatureDefinition.parse_file(feature_definition)
        # create virtual file systm directory using easyfs
        virtual_dir = Directory()
        virtual_dir["src"] = SrcDir.from_definition_model(
            definition_model=definition_model, nanolayer_version=nanolayer_version
        )
        virtual_dir["test"] = TestDir.from_definition_model(
            definition_model=definition_model
        )

        # manifesting the virtual directory into local filesystem
        virtual_dir.create(output_dir)

        for file_path in  glob.glob(os.path.join(output_dir, "test",str(definition_model.id), "*.sh")):
            os.chmod(file_path, int("755", base=8))

        for file_path in  glob.glob(os.path.join(output_dir, "src",str(definition_model.id),"install.sh")):
            os.chmod(file_path, int("755", base=8))
