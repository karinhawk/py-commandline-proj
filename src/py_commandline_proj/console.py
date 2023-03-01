import textwrap

import click

#because this was imported using poetry I need to configure what interpretter python is using
#bc vscode doesn't automatically know if you're using a virtual env
import requests

from . import __version__




# @click.command()
# @click.version_option(version=__version__)
# def main():
#     """python time"""
#     click.echo("Hello, world!")

#api to grab a random fact from wikipedia!
API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

@click.command()
@click.version_option(version=__version__)

#creates new function - use click.group if you want to group functions together in separate package thing
def main():
    """python time!!"""
    #requests.get is a fetch for url
    #with closes the https connection at the end of the block
    with requests.get(API_URL, verify=False) as response:
        response.raise_for_status()
        data = response.json()

    #accessing keyvalue pairs using index title - data is json
    title = data["title"]
    extract = data["extract"]
    #outputs to console, but with style! can change colours and size and stuff (style echo = secho)
    click.secho(title, fg="green")
    #outputs to console
    #textwrap literally just wraps the text - can specify width of characters
    click.echo(textwrap.fill(extract))

    


