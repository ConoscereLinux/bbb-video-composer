import os
import pathlib
import shutil

import typer

from . import composer, constants, downloader


cli = typer.Typer()


@cli.command()
def download(recording_url: str, project_name: str = None, skip_existing: bool = True):
    dw = downloader.Downloader(recording_url, project_name)

    typer.echo(f"Downloading all needed files in {dw.root_path}")
    dw.download_all(skip_existing)


@cli.command()
def clean(project_id: str = None):
    for project in constants.DATA_PATH.glob(project_id if project_id else "*"):
        if project.is_file():
            continue

        typer.echo(f"Deleting folder {project}? [yN]")
        if input() in {"y", "Y"}:
            shutil.rmtree(project)


@cli.command()
def compose(
    project_id: str,
    bg_image: pathlib.Path = "assets/bg-clinux_720p.png",
    title: str = "",
    relator: str = "",
    preview: bool = False,
    start: int = None,
    duration: int = None,
):
    size = (1280, 720)
    font = "Open-Sans-Regular"

    c = composer.Composer(project_id, size=size)

    webcam = (400, 300)
    desk_share = (813, 457)

    c.add_background_image(bg_image)

    c.add_desk_share(desk_share, (440, 120))
    c.add_webcam(webcam, (27, 120))

    if title:
        c.add_text(
            title, (1226, 50), (27, 35), color="white", font=font, stroke_color="white"
        )

    if relator:
        c.add_text(relator, (384, 54), (35, 480), color="white", font=font)

    if preview:
        c.preview()
    else:
        c.render(start=start, duration=duration, fps=24, threads=os.cpu_count())
