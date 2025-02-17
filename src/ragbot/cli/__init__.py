import typer

from .milvus_cli import cli as milvus_cli

app = typer.Typer(
    name="Ragbot CLI",
    help="Ragbot tools.",
    add_completion=True,
    pretty_exceptions_enable=True,
)


app.add_typer(milvus_cli, name="milvus")


if __name__ == "__main__":
    app()
