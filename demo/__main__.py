import argparse
import pathlib
import re
import urllib.parse
import urllib.request

import requests

# import xml.etree.ElementTree as ET


DATA_PATH = pathlib.Path(".data")


class Downloader:
    VALID_URL_REGEX = re.compile(
        r"^(?P<base>.*)/playback/presentation/2\.[03]/"
        r"(?:playback\.html\?meetingId=)?(?P<id>\S+)$"
    )

    def __init__(self, url: str):
        self._url = url

        if not (match := self.VALID_URL_REGEX.fullmatch(url)):
            raise ValueError("Invalid URL")

        self._base = match.group("base")
        self._id = match.group("id")

        self.out_dir = DATA_PATH / self._id
        self.out_dir.mkdir(exist_ok=True)

    def download(self, endpoint: str):
        url = urllib.parse.urljoin(self._base, f"/presentation/{self._id}/{endpoint}")
        out = self.out_dir / endpoint
        with open(out, "wb") as fp:
            response = requests.get(url, allow_redirects=True)
            fp.write(response.content)
        return out

    def download_all(self):
        self.download("metadata.xml")

        # doc = ET.parse(self.download("shapes.svg"))
        # for img in doc.iterfind(".//{http://www.w3.org/2000/svg}image"):
        #     self.download(img.get("{http://www.w3.org/1999/xlink}href"))

        for endpoint in (
            # "panzooms.xml",
            # "cursor.xml",
            # "deskshare.xml",
            # "presentation_text.json",
            # "captions.json",
            # "slides_new.xml",
            # "video/webcams.webm",
            # "deskshare/deskshare.webm",
        ):
            self.download(endpoint)


parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("project_name")

args = parser.parse_args()


PROJECT_PATH = DATA_PATH / args.project_name
PROJECT_PATH.mkdir(exist_ok=True)


Downloader(args.url).download_all()
