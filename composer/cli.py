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


def _prepare_course(project_id: str, bg_image: pathlib.Path, title: str, relator: str):
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

    return c


@cli.command()
def compose(
    project_id: str,
    bg_image: pathlib.Path = "assets/bg-clinux_720p.png",
    title: str = "",
    relator: str = "",
    preview: bool = False,
    start: float = None,
    duration: float = None,
):
    c = _prepare_course(project_id, bg_image, title, relator)

    if preview:
        c.preview()
    else:
        c.render(start=start, duration=duration, threads=os.cpu_count())


@cli.command()
def parts(
    project_id: str,
    n_parts: int,
    only_part: int = None,
    bg_image: pathlib.Path = "assets/bg-clinux_720p.png",
    title: str = "",
    relator: str = "",
):
    c = _prepare_course(project_id, bg_image, title, relator)
    duration = c.duration / n_parts

    for i in range(n_parts):
        if only_part and only_part != i:
            continue

        start = i * duration

        path = str(constants.DATA_PATH / project_id / f"out_{i:02}.mp4")
        c.render(path, start=start, end=start + duration, threads=os.cpu_count())
