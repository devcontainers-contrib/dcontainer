import os
import pathlib

import pytest
from helpers import FEATURE_DEFINITION_DIR

from dcontainer.devcontainer.feature_generation.oci_feature_generator import (
    OCIFeatureGenerator,
)

TEST_FEATURE_IDS = (
    "actions-runner",
    "actions-runner-noruntime-no-externals",
    "powershell",
    "ansible",
    "pnpm",
    "alp-asdf",
    "act-asdf",
    "kotlin-sdkman",
    "asdf-package",
    "angular-cli",
    "npm-package",
    "apt-get-packages",
    "apt-packages",
    "caddy",
    "brownie",
    "caddy",
    "cosign",
    "gh-release",
    "groovy-sdkman",
    "immuadmin",
    "immuadmin-fips",
    "localstack",
    "micronaut-sdkman",
)
# TEST_FEATURE_IDS = ["direnv"]

TEST_FEATURE_PATHS = [
    (v, os.path.join(FEATURE_DEFINITION_DIR, v), "v0.5.0")
    for v in os.listdir(FEATURE_DEFINITION_DIR)
    if v in TEST_FEATURE_IDS
]


TEST_IMAGE = "mcr.microsoft.com/devcontainers/base:debian"


@pytest.mark.parametrize(
    "feature_id,feature_definition_dir,nanolayer_version",
    TEST_FEATURE_PATHS,
)
def test_feature_dir_generation(
    shell,
    tmp_path: pathlib.Path,
    feature_id: str,
    feature_definition_dir: str,
    nanolayer_version: str,
) -> None:
    feature_definition = os.path.join(feature_definition_dir, "feature-definition.json")

    tmp_path_str = tmp_path.as_posix()
    OCIFeatureGenerator.generate(
        feature_definition=feature_definition,
        output_dir=tmp_path.as_posix(),
        nanolayer_version=nanolayer_version,
    )

    assert os.path.isfile(
        os.path.join(tmp_path_str, "test", feature_id, "scenarios.json")
    )
    assert os.path.isfile(
        os.path.join(tmp_path_str, "src", feature_id, "library_scripts.sh")
    )
    assert os.path.isfile(
        os.path.join(tmp_path_str, "src", feature_id, "devcontainer-feature.json")
    )
    assert os.path.isfile(os.path.join(tmp_path_str, "src", feature_id, "install.sh"))
    assert os.path.isfile(os.path.join(tmp_path_str, "src", feature_id, "README.md"))


@pytest.mark.parametrize(
    "feature_id,feature_definition_dir,nanolayer_version",
    TEST_FEATURE_PATHS,
)
def test_feature_dir_generation_and_run_devcontainer_tests(
    shell,
    tmp_path: pathlib.Path,
    feature_id: str,
    feature_definition_dir: str,
    nanolayer_version: str,
) -> None:
    feature_definition = os.path.join(feature_definition_dir, "feature-definition.json")

    tmp_path_str = tmp_path.as_posix()
    OCIFeatureGenerator.generate(
        feature_definition=feature_definition,
        output_dir=tmp_path_str,
        nanolayer_version=nanolayer_version,
    )
    cmd = f"BUILDKIT_PROGRESS=plain devcontainer features test -p {tmp_path_str} -f {feature_id} --skip-autogenerated"
    print(cmd)
    response = shell.run(
        cmd,
        shell=True,
    )
    print(response.stdout)
    print(response.stderr)

    assert response.returncode == 0
