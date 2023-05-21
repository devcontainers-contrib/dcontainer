import logging
from typing import Dict, Optional, Union

from easyfs import File
from nanolayer.installers.devcontainer_feature.oci_feature import OCIFeature

from dcontainer.devcontainer.models.devcontainer_feature import FeatureOption
from dcontainer.devcontainer.models.devcontainer_feature_definition import (
    FeatureDependencies,
)
from dcontainer.utils.version import resolve_nanolayer_release_version

logger = logging.getLogger(__name__)


SINGLE_DEPENDENCY = """$nanolayer_location \\
    install \\
    devcontainer-feature \\
    "{feature_oci}" {stringified_envs_args}
    
"""

HEADER = """#!/bin/bash -i

set -e

source ./library_scripts.sh

# nanolayer is a cli utility which keeps container layers as small as possible
# source code: https://github.com/devcontainers-contrib/nanolayer
# `ensure_nanolayer` is a bash function that will find any existing nanolayer installations, 
# and if missing - will download a temporary copy that automatically get deleted at the end 
# of the script
ensure_nanolayer nanolayer_location "{nanolayer_version}"


{dependency_installation_lines}

{install_command}

"""


class InstallSH(File):
    REF_PREFIX = "$options."
    ENTRYPOINTS_BASE_LOCATION = "/usr/local/share"

    def __init__(
        self,
        install_command: str,
        dependencies: Optional[FeatureDependencies],
        options: Optional[Dict[str, FeatureOption]],
        nanolayer_version: Optional[str] = None,
    ) -> None:
        self.install_command = install_command
        self.dependencies = dependencies or []
        self.options = options
        try:
            self.nanolayer_version = (
                nanolayer_version or resolve_nanolayer_release_version()
            )
        except Exception as e:
            raise ValueError(
                "could not resolve nanolayer version because of error, please manually set nanolayer_version release_verison"
            ) from e

        super().__init__(content=self.to_str().encode())

    def to_str(self) -> str:
        installation_lines = []
        for feature_dependency in self.dependencies:
            resolved_params = {}
            for param_name, param_value in feature_dependency.options.items():
                if isinstance(param_value, str):
                    if InstallSH.is_param_ref(param_value):
                        param_value = f'"{InstallSH.resolve_param_ref( param_value, self.options )}"'
                    else:
                        param_value = f"'{param_value}'"
                elif isinstance(param_value, bool):
                    param_value = f"'{str(param_value).lower()}'"

                else:
                    raise ValueError(
                        f"param {param_value} is of bad type: {str(type(param_value))} (only string or boolean allowed)"
                    )

                resolved_params[param_name] = param_value

            installation_lines.append(
                self.create_install_command(feature_dependency.feature, resolved_params)
            )
        dependency_installation_lines = "\n\n".join(installation_lines)

        return HEADER.format(
            dependency_installation_lines=dependency_installation_lines,
            install_command=self.install_command,
            nanolayer_version=self.nanolayer_version,
        )

    @staticmethod
    def _escape_qoutes(value: str) -> str:
        return value.replace('"', '\\"')

    @classmethod
    def is_param_ref(cls, param_value: str) -> bool:
        return param_value.startswith(cls.REF_PREFIX)

    def create_install_command(self, feature_oci: str, params: Dict[str, str]) -> str:
        stringified_envs_args = " ".join(
            [f"--option {env}={val}" for env, val in params.items()]
        )

        stringified_envs_args = f"\\\n {stringified_envs_args}"

        return SINGLE_DEPENDENCY.format(
            stringified_envs_args=stringified_envs_args, feature_oci=feature_oci
        )

    @classmethod
    def resolve_param_ref(
        cls, param_ref: str, options: Optional[Dict[str, FeatureOption]]
    ) -> str:
        if options is None:
            raise ValueError(
                f"option reference was given: '{param_ref}' but no options exists"
            )

        option_name = param_ref.replace(cls.REF_PREFIX, "")

        option = options.get(option_name, None)
        if option is None:
            raise ValueError(
                f"could not resolve option reference: '{param_ref}' please ensure you spelled the option name right ({option})"
            )
        return f"${option_name}".upper()
