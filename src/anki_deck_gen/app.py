from typing import Annotated

import typer

__all__ = ["app"]

app = typer.Typer()


@app.command()
def l_odyssee():
    from .l_odyssee.app import app

    app()


@app.command()
def ascii(upper_bound: int = 128, extended_ascii: bool = False):
    import anki_deck_gen.ascii_codes as ascii_codes

    if extended_ascii:
        upper_bound = 256

    ascii_codes.generate_deck(upper_bound=upper_bound)


@app.command(help="Generates random IDs between 2^30 and 2^31.")
def gen_id(count: Annotated[int, typer.Argument()] = 1):
    from .genanki_ext import random_id

    for _ in range(count):
        print(random_id())
