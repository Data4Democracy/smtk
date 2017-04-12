import click
import click_completion

import smtk.utils.logger as l

from smtk.commands.cli import TargetCommand
from smtk.commands.cli import TwitterCommand
from smtk.commands.cli import GoogleCommand

click_completion.init()


@click.group()
def main(**kwargs):
    l.INFO("Starting SMTK")


@main.command(cls=TargetCommand)
def target():
    l.INFO("Target Command Detected")


@main.command(cls=TwitterCommand)
def twitter():
    l.INFO("Twitter Command Detected")


@main.command(cls=GoogleCommand)
def google():
    l.INFO("Google Command Detected")


if __name__ == '__main__':
    main()
