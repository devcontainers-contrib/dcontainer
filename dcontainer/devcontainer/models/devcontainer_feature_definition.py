from __future__ import annotations

from typing import Dict, List, Optional, Union
from unittest import mock

from nanolayer.installers.devcontainer_feature.oci_feature import OCIFeature
from pydantic import BaseModel, Extra, Field

from dcontainer.devcontainer.models.devcontainer_feature import Feature


class FeatureDependency(BaseModel):
    feature: str
    options: Dict[str, Union[bool, str]]


class TestScenario(BaseModel):
    name: str
    image: str
    test_commands: List[str]
    options: Dict[str, Union[str, bool]]


class FeatureDependencies(BaseModel):
    __root__: List[FeatureDependency]

    def __iter__(self):
        return iter(self.__root__)

    def __len__(self):
        return len(self.__root__)

    def __getattr__(self, k):
        return getattr(self.__root__, k)


class FeatureDefinition(Feature):
    class Config:
        extra = Extra.ignore

    dependencies: Optional[FeatureDependencies] = Field(
        None,
        description="Possible user-configurable feature dependencies for this Feature. The selected features and their params will be installed prior to running the installation command",
    )

    install_command: Optional[str] = Field(
        None,
        description="This command will be run after dependencies are all installed",
    )

    test_scenarios: List[TestScenario] = Field(
        None,
        description="List of test scenarios to prepare testing different use cases",
    )

    def to_feature_model(self) -> Feature:
        if self.dependencies is not None:

            for dependency in self.dependencies:
                dependency_feature_obj: Feature = (
                    OCIFeature.get_devcontainer_feature_obj(dependency.feature)
                )
                if (
                    dependency_feature_obj.privileged is not None
                    and dependency_feature_obj.privileged
                ):
                    self.privileged = True

                if dependency_feature_obj.mounts is not None:
                    if self.mounts is None:
                        self.mounts = []

                    stringified_mounts = [
                        mount.json(sort_keys=True) for mount in self.mounts
                    ]
                    for mount_dict in dependency_feature_obj.mounts:
                        if mount_dict.json(sort_keys=True) not in stringified_mounts:
                            self.mounts.append(mount_dict)

                if dependency_feature_obj.entrypoint is not None:
                    if self.entrypoint is None or self.entrypoint == "":
                        self.entrypoint = dependency_feature_obj.entrypoint
                    else:

                        self.entrypoint += f"&& {dependency_feature_obj.entrypoint}"
                        
        with mock.patch.object(Feature.Config, "extra", Extra.ignore):
            return Feature.parse_raw(self.json())
