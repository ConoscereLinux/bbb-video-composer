import argparse
import pathlib

import requests

DATA_PATH = pathlib.Path(".data")


parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("project_name")

args = parser.parse_args()


PROJECT_PATH = DATA_PATH / args.project_name
PROJECT_PATH.mkdir(exist_ok=True)

