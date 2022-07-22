import typer

from app import setup

app = typer.Typer()


@app.command(name="hello")
def hello(name: str) -> None:
    typer.echo(f"Hello world {name}")


@app.callback()
def callback() -> None:
    """
    We use callback here to force subcommand, event we have only one command defined
    """
    pass


if __name__ == "__main__":
    setup.setup_logging()
    setup.setup_error_reporting()
    app()
