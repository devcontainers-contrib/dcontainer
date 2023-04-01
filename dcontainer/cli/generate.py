import logging
import pathlib
from typing import Optional

import typer

from dcontainer.devcontainer.feature_generation.oci_feature_generator import (
    OCIFeatureGenerator,
)

logger = logging.getLogger(__name__)

app = typer.Typer(pretty_exceptions_show_locals=False, pretty_exceptions_short=False)

app.command()


@app.command("devcontainer-feature")
def generate_command(
    feature_definition: pathlib.Path,
    output_dir: pathlib.Path,
    release_version: Optional[str] = None,
) -> None:
    OCIFeatureGenerator.generate(
        feature_definition=feature_definition.as_posix(),
        output_dir=output_dir.as_posix(),
        nanolayer_version=release_version,
    )
