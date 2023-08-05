import click
import toml
from progressbar import progressbar
import twitter
import sys

from . import __version__


@click.command()
@click.version_option(version=__version__)
@click.option("--export/--no-export", default=False)
@click.option("--list/--no-list", default=False)
@click.argument("filename")
def main(export, list, filename):

    api = twitter.Api(**toml.load("twitter_keys.toml"))

    if export:
        with open(filename, "w") as f:
            for user in api.GetBlocks():
                f.write(str(user.id) + "\n")
        sys.exit(0)

    if list:
        user_ids = [
            user.id
            for user in api.GetListMembersPaged(list_id=int(filename), count=10000, skip_status=True)[2]
        ]
    else:
        with open(filename, "r") as f:
            user_ids = [l.strip() for l in f.readlines()]

    for user_id in progressbar(user_ids, redirect_stdout=True):
        try:
            api.CreateBlock(user_id=int(user_id))
        except Exception as e:
            print(e)
