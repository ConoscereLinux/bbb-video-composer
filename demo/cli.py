import click
from loguru import logger

from . import composer, downloader


@click.group()
def cli():
    pass


@cli.command("")
@click.option("--project-name", default=None)
@click.argument("recording_url")
@click.option("--skip-existing/--no-skip-existing", default=True)
def download(project_name, recording_url, skip_existing):
    dw = downloader.Downloader(recording_url, project_name)

    logger.info(f"Downloading all needed files in {dw.root_path}")
    dw.download_all(skip_existing)


@cli.command()
@click.argument("project_id")
def compose(project_id):
    composer.Composer(project_id).compose()
