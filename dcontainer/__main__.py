import typer

from dcontainer.cli.generate import app as generate_app
from dcontainer.utils.version import (
    resolve_own_package_version,
)

app = typer.Typer(pretty_exceptions_show_locals=False, pretty_exceptions_short=False)
app.add_typer(generate_app, name="generate")


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"dcontainer version: {resolve_own_package_version()}")
        raise typer.Exit()


@app.callback()
def version(
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    )
):
    return


def main() -> None:
    app()


if __name__ == "__main__":
    main()
