from pathlib import Path
from dcontainer.devcontainer.models.devcontainer_feature import FeatureOptionItem2
from dcontainer.devcontainer.models.devcontainer_feature_definition import (
    FeatureDefinition,
    FeatureDependencies,
    FeatureDependency,
    TestScenario,
)

import os


def generate_apt_get_definitions(partial_feature_json: str, output_dir: str) -> None:
    with open(partial_feature_json, "r") as f:
        import json

        partial_features = json.load(f)

    for partial_feature in partial_features:
        feature_definition_file = os.path.join(
            output_dir, partial_feature["id"], "feature-definition.json"
        )

        Path(feature_definition_file).parent.mkdir(parents=True, exist_ok=True)

        feature_definition = FeatureDefinition(
            id=partial_feature["id"],
            name=f"{partial_feature['name']} (via apt-get)",
            version="1.0.0",
            description=partial_feature["description"],
            documentationURL=f"http://github.com/devcontainers-contrib/features/tree/main/src/{partial_feature['id']}",
            installsAfter=["ghcr.io/devcontainers-contrib/features/apt-get-packages"],
            dependencies=
                FeatureDependencies(__root__=[
                    FeatureDependency(feature="ghcr.io/devcontainers-contrib/features/apt-get-packages:1.0.2",
                    options={
                        "packages": partial_feature["package"],
                    },
                )])
            ,
            install_command="echo 'Done!'",
            test_scenarios=[
                TestScenario(
                    name="test_defaults_debian",
                    image="mcr.microsoft.com/devcontainers/base:debian",
                    test_commands=[partial_feature["test_command"]],
                    options={}
                )
            ],
            options={
            },
        )

        with open(feature_definition_file, "w+") as f:
            f.write(feature_definition.json(exclude_none=True, indent=4))


if __name__ == "__main__":
    generate_apt_get_definitions(
        partial_feature_json="/workspaces/dcontainer/dev/apt-get-features/apt_get_partial_features.json",
        output_dir="/workspaces/dcontainer/tests/resources/new_features",
    )
