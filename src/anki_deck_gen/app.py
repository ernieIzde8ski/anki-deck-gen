import typer

__all__ = ["app"]

app = typer.Typer()


@app.command()
def l_odyssee():
    from .l_odyssee.app import app

    app()
