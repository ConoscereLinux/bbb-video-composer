import argparse
import pathlib
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import moviepy.editor
import requests

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

    @property
    def project_id(self) -> str:
        return self._id

    def download(self, endpoint: str):
        url = urllib.parse.urljoin(self._base, f"/presentation/{self._id}/{endpoint}")

        out = self.out_dir / endpoint
        if out.exists():
            return out

        out.parent.mkdir(parents=True, exist_ok=True)
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
            "deskshare.xml",
            # "presentation_text.json",
            # "captions.json",
            # "slides_new.xml",
            "video/webcams.webm",
            "deskshare/deskshare.webm",
        ):
            self.download(endpoint)


class Composer:
    def __init__(self, project_id: str):
        self._id = project_id
        self._base_dir = DATA_PATH / self._id

        self.size = (1920, 1080)
        self._clips = []

        self._prepare_webcam()
        self._prepare_deskshare()

    def compose(self):
        if self._clips:
            movie = moviepy.editor.CompositeVideoClip(self._clips, size=self.size)
            movie = movie.set_duration(30)
            movie.write_videofile(str(self._base_dir / "out.mp4"))

    def _prepare_webcam(self):
        video_url = str(self._base_dir / "video" / "webcams.webm")
        video = moviepy.editor.VideoFileClip(video_url)
        self._clips.append(video)

    def _prepare_deskshare(self):
        events = ET.parse(self._base_dir / "deskshare.xml").findall("./event")
        if not events:
            return

        video_url = str(self._base_dir / "deskshare" / "deskshare.webm")
        video = moviepy.editor.VideoFileClip(video_url)

        for event in events:
            t_start = float(event.get("start_timestamp"))
            t_stop = float(event.get("stop_timestamp"))
            clip = video.subclip(t_start, t_stop)
            self._clips.append(clip.set_position((self.size[0] - clip.size[0], 0)))


parser = argparse.ArgumentParser()
parser.add_argument("url")

args = parser.parse_args()


(d := Downloader(args.url)).download_all()

Composer(d.project_id).compose()
