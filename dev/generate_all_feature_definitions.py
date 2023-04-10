import os
from typing import Optional
from dcontainer.devcontainer.feature_generation.oci_feature_generator import OCIFeatureGenerator
from pathlib import Path
from dcontainer.devcontainer.models.devcontainer_feature_definition import (
    FeatureDefinition,
)
import typer
import shutil


def is_dependent_of(feature_name: str, feature_definition: FeatureDefinition) -> bool:
    if feature_definition.dependencies is not None:
        for dep in feature_definition.dependencies:
            if feature_name in dep.feature:
                return True
    
    return False

def generate_all_Feature_definitions(
    feature_definitions_dir: str, output_dir: str ,nanolayer_version: str, remove_old_content: bool = True,  depends_on: Optional[str] = None
) -> None:
    assert nanolayer_version.startswith("v")
    
    for feature_name in os.listdir(feature_definitions_dir):
        feature_definition_file = os.path.join(
                    feature_definitions_dir, feature_name, "feature-definition.json"
                )
        feature_definition = FeatureDefinition.parse_file(feature_definition_file)

        if depends_on is not None and not is_dependent_of(depends_on, feature_definition):
            continue

        if remove_old_content and os.path.exists(os.path.join(
                    "test", feature_name
                ) ):
            shutil.rmtree(os.path.join(
                        "test", feature_name
                    )
                    )
        if remove_old_content and os.path.exists(os.path.join(
                    "src", feature_name
                ) ):
            shutil.rmtree(os.path.join(
                        "src", feature_name
                    )
                    )

        OCIFeatureGenerator.generate(
            Path(
                feature_definition_file
            ),
            output_dir=Path(output_dir),
            nanolayer_version=nanolayer_version
        )


if __name__ == "__main__":
    typer.run(generate_all_Feature_definitions)
