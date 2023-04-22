import os
from enum import Enum
from pathlib import Path
from typing import Optional

import semver
import typer

from dcontainer.devcontainer.models.devcontainer_feature_definition import (
    FeatureDefinition,
)


class VersionType(Enum):
    patch = "patch"
    minor = "minor"
    major = "major"


def is_dependent_of(feature_name: str, feature_definition: FeatureDefinition) -> bool:
    if feature_definition.dependencies is not None:
        for dep in feature_definition.dependencies:
            if feature_name in dep.feature:
                return True

    return False


def bump_version_feature_definitions(
    feature_definitions_dir: str,
    version_type: VersionType,
    depends_on: Optional[str] = None,
) -> None:
    for feature_name in os.listdir(feature_definitions_dir):
        feature_definition_file = os.path.join(
            feature_definitions_dir, feature_name, "feature-definition.json"
        )

        feature_definition = FeatureDefinition.parse_file(feature_definition_file)

        if depends_on is not None and not is_dependent_of(
            depends_on, feature_definition
        ):
            continue

        semver_version = semver.VersionInfo.parse(feature_definition.version)

        if version_type == VersionType.patch:
            bumped_semver = semver_version.bump_patch()
        elif version_type == VersionType.minor:
            bumped_semver = semver_version.bump_minor()

        elif version_type == VersionType.major:
            bumped_semver = semver_version.bump_major()
        else:
            raise ValueError(f"invalid version type: {version_type}")

        feature_definition.version = str(bumped_semver)

        with open(feature_definition_file, "w+") as f:
            f.write(feature_definition.json(exclude_none=True, indent=4))


if __name__ == "__main__":
    typer.run(bump_version_feature_definitions)
