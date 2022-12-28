import os

import click
from colorama import Fore, Style


def get_vars(path):
    """Get all the variables from the .env file"""
    with open(path, "r") as f:
        content = f.read()
    lines = content.splitlines()
    lines = [line for line in lines if line and not line.startswith("#")]
    return {line.split("=")[0]: line.split("=")[1] for line in lines}


@click.command(name="new")
@click.option("--name", "-n", help="Name of the environment variable")
@click.option(
    "--development",
    "-d",
    help="Value of the environment variable for the development environment",
)
@click.option(
    "--production",
    "-p",
    help="Value of the environment variable for the production environment",
)
def add_variable(name, development, production):
    if not name:
        raise click.ClickException(
            Fore.RED
            + "Name of the environment variable is not provided"
            + Style.RESET_ALL
        )

    if (
        name in get_vars(".env.development").keys()
        or name in get_vars(".env.production").keys()
    ):
        raise click.ClickException(
            Fore.RED + "The environment variable with this name already "
            "exists" + Style.RESET_ALL
        )

    if not development:
        development = click.prompt(
            "Value of the environment variable for the development environment",
            hide_input=True,
        )

    if not production:
        production = click.prompt(
            "Value of the environment variable for the production environment",
            hide_input=True,
        )

    with open("./.env.development", "a") as f:
        f.write(f"\n{name}={development}")

    with open("./.env.production", "a") as f:
        f.write(f"\n{name}={production}")

    # Success message
    click.echo(
        Fore.GREEN
        + f"Environment variable {name} has been successfully added"
        + Style.RESET_ALL
    )


@click.command(name="init")
def create_files():
    """Create .env.development and .env.production files from template files"""
    if os.path.exists("./.env.development"):
        raise click.ClickException(
            Fore.RED
            + "File .env.development already exists!"
            + Style.RESET_ALL
        )

    if os.path.exists("./.env.production"):
        raise click.ClickException(
            Fore.RED + "File .env.production already exists!" + Style.RESET_ALL
        )

    dev_token = click.prompt(
        "Enter the Discord bot token for the development environment", type=str
    )
    prod_token = click.prompt(
        "Enter the Discord bot token for the production environment (skip)",
        type=str,
    )

    if prod_token == "skip":
        prod_token = "REQUIRED_PRODUCTION_TOKEN"

    development_content = "DISCORD_TOKEN={}\nSTATE_NAME=DEVELOPMENT".format(
        dev_token
    )
    production_content = "DISCORD_TOKEN={}\nSTATE_NAME=PRODUCTION".format(
        prod_token
    )

    with open("./.env.development", "w") as f:
        f.write(development_content)

    with open("./.env.production", "w") as f:
        f.write(production_content)

    # Success message
    click.echo(
        Fore.GREEN
        + "Files .env.development and .env.production have been created"
        + Style.RESET_ALL
    )


@click.group()
def cli():
    pass


cli.add_command(add_variable)
cli.add_command(create_files)

if __name__ == "__main__":
    cli()
