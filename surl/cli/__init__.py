import typer
from rich import print
from sqlalchemy.future import select

from app import schemas
from app.core.config import Settings, get_settings
from app.db import crud, models
from app.db.session import async_session_factory

from .db import db

cli = typer.Typer(name="surl", add_completion=False)
cli.add_typer(db, name="db")


@cli.command()
def settings() -> None:
    settings: Settings = get_settings()
    print(settings.dict())


@cli.command()
def shell() -> None:  # pragma: no cover
    """Opens an interactive shell with objects auto imported"""
    settings: Settings = get_settings()
    _vars = {
        "settings": settings,
        "async_session_factory": async_session_factory,
        "select": select,
        "models": models,
        "crud": crud,
        "schemas": schemas,
    }
    print(f"Auto imports: {list(_vars.keys())}")
    try:
        from IPython import start_ipython

        start_ipython(argv=[], user_ns=_vars)
    except ImportError:
        import code

        code.InteractiveConsole(_vars).interact()


# @cli.command()
# def db() -> None:
#     asyncio.run()


cli()
