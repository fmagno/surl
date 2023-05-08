import asyncio

import typer

from .prune import prune_aio
from .seed import seed_aio

db = typer.Typer(name="db", add_completion=False)


# cli db prune
# cli db seed --prune --num-employees 10 --num-shops 10 --num-tools 10 --seed 0


@db.command()
def prune() -> None:
    asyncio.run(prune_aio())


@db.command()
def seed() -> None:
    asyncio.run(seed_aio())
