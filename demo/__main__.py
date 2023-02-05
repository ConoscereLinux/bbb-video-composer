import argparse
import pathlib

from . import composer, download

DATA_PATH = pathlib.Path(".data")


parser = argparse.ArgumentParser()
parser.add_argument("url")

args = parser.parse_args()


(d := download.Downloader(args.url)).download_all()

composer.Composer(d.project_id).compose()
