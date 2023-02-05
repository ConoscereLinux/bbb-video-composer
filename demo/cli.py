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
@click.option("--bg-image", default=None)
def compose(project_id, bg_image):
    size = (1920, 1080)
    palette = dict(white="#ffffff", cyan="#5599ff", blue="#447bcd")

    c = composer.Composer(project_id, size=size)

    webcam = (600, 450)
    desk_share = (1220, 686)
    # text_block = (480, (desk_share[1] - webcam[1]) // 2 - border)

    c.add_background_image(bg_image if bg_image else "assets/bg-clinux.png")

    c.add_desk_share(desk_share, (660, 190))
    c.add_webcam(webcam, (40, 190))

    # c.add_text(
    #     "A very very very \nvery long Title",
    #     text_block,
    #     (border, webcam[1] + 2 * border),
    #     color=palette["white"],
    #     bg_color=palette["blue"],
    #     font="open-sans",
    # )

    # c.add_text(
    #     "Name Surname",
    #     text_block,
    #     (border, webcam[1] + text_block[1] + 3 * border),
    #     color=palette["white"],
    #     bg_color=palette["blue"],
    # )

    c.compose(5)
