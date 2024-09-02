import typer

from .add import add

__all__ = ["app"]

app = typer.Typer()


@app.command()
def l_odyssee():
    from .l_odyssee.app import app

    app()


@app.command(name="add")
def add_input(left: int, right: int) -> None:
    res: int = add(left, right)
    print(res)
