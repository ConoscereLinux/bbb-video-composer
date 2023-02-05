import xml.etree.ElementTree as ET

import moviepy.editor

from .constants import DATA_PATH


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
