import shutil

import click
from loguru import logger

from . import composer, constants, downloader


@click.group()
def cli():
    pass


@cli.command()
@click.option("--project-name", default=None)
@click.argument("recording_url")
@click.option("--skip-existing/--no-skip-existing", default=True)
def download(project_name, recording_url, skip_existing):
    dw = downloader.Downloader(recording_url, project_name)

    logger.info(f"Downloading all needed files in {dw.root_path}")
    dw.download_all(skip_existing)


@cli.command()
@click.option("--project-id", default=None)
def clean(project_id):
    for project in constants.DATA_PATH.glob(project_id if project_id else "*"):
        if project.is_file():
            continue

        click.echo(f"Deleting folder {project}? [yN]")
        if input() in {"y", "Y"}:
            shutil.rmtree(project)


@cli.command()
@click.argument("project_id")
@click.option("--bg-image", default=None)
@click.option("--title", default=None)
@click.option("--relator", default=None)
@click.option("--preview/--no-preview", default=False)
def compose(project_id, bg_image, title, relator, preview):
    size = (1920, 1080)
    font = "Open-Sans-Regular"

    c = composer.Composer(project_id, size=size)

    webcam = (600, 450)
    desk_share = (1220, 686)

    c.add_background_image(bg_image if bg_image else "assets/bg-clinux.png")

    c.add_desk_share(desk_share, (660, 180))
    c.add_webcam(webcam, (40, 180))

    if title:
        c.add_text(
            title, (1820, 80), (40, 50), color="white", font=font, stroke_color="white"
        )

    if relator:
        c.add_text(relator, (560, 80), (60, 720), color="white", font=font)

    if preview:
        c.preview()
    else:
        c.render(5)
