"""Application runner."""

from .database.services.setup.database_setup import run_db_setup
from .frontend.cli import CLI


def run():
    run_db_setup()

    # Run the CLI application
    cli = CLI()
    cli.run()
