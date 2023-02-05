import re
import urllib.parse

import requests
from loguru import logger

from .constants import DATA_PATH


class Downloader:
    VALID_URL_REGEX = re.compile(
        r"^(?P<base>.*)/playback/presentation/2\.[03]/"
        r"(?:playback\.html\?meetingId=)?(?P<id>\S+)$"
    )

    def __init__(self, url: str, name: str = None):
        self._url = url

        if not (match := self.VALID_URL_REGEX.fullmatch(url)):
            raise ValueError("Invalid URL")

        self._base = match.group("base")
        self._id = match.group("id")
        self._name = name if name else self._id

        self._out_dir = DATA_PATH / self._name
        self._out_dir.mkdir(exist_ok=True)

    @property
    def project_id(self) -> str:
        return self._id

    @property
    def root_path(self):
        return self._out_dir

    def download(self, endpoint: str, skip_existing=True):
        url = urllib.parse.urljoin(self._base, f"/presentation/{self._id}/{endpoint}")

        out = self._out_dir / endpoint
        if skip_existing and out.exists():
            logger.info(f"(skipping) {out} already exists, skipping")
            return out

        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "wb") as fp:
            response = requests.get(url, allow_redirects=True)
            fp.write(response.content)

        logger.info(f"(downloaded) {out}")
        return out

    def download_all(self, skip_existing=True):
        self.download("metadata.xml", skip_existing)

        # doc = ET.parse(self.download("shapes.svg"))
        # for img in doc.iterfind(".//{http://www.w3.org/2000/svg}image"):
        #     self.download(img.get("{http://www.w3.org/1999/xlink}href"))

        for endpoint in (
            # "panzooms.xml",
            # "cursor.xml",
            "deskshare.xml",
            "presentation_text.json",
            # "captions.json",
            # "slides_new.xml",
            "video/webcams.webm",
            "deskshare/deskshare.webm",
        ):
            self.download(endpoint, skip_existing)
