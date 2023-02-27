import pathlib
import xml.etree.ElementTree as ET

import moviepy.editor
import moviepy.video

from .constants import DATA_PATH

Size = tuple[int, int]
Position = tuple[int, int]
Time = float | tuple[int, int] | tuple[int, int, int] | str


def hex_to_rgb(color: str):
    color = color.lstrip("#")
    if len(color) == 3:
        color = color[0] * 2 + color[1] * 2 + color[2] * 2
    return int(color[0:2], 16), int(color[2:4], 16), int(color[4:], 16)


class Composer:
    def __init__(self, project_id: str, size: tuple[int, int] = (1920, 1080)):
        self._id = project_id
        self._base_dir = DATA_PATH / self._id

        self.size = size
        self.metadata = ET.parse(str(self._base_dir / "metadata.xml")).getroot()

        self._clips = []

    @property
    def duration(self):
        return float(self.metadata.find("playback/duration").text) / 1000

    def preview(self):
        movie = moviepy.editor.CompositeVideoClip(self._clips, size=self.size)
        movie.save_frame(str(self._base_dir / "out.png"), t=0)

    def render(
        self,
        path: str = None,
        /,
        fps: int = 24,
        duration: Time = None,
        start: Time = 0,
        end: Time = None,
        **kwargs,
    ):
        if not self._clips:
            raise Exception("You need to add at least one clip")

        movie = moviepy.editor.CompositeVideoClip(self._clips, size=self.size)
        movie = movie.set_duration(duration if duration else self.duration)
        if start or end:
            movie = movie.subclip(t_start=start, t_end=end)

        if path is None:
            path = str(self._base_dir / "out.mp4")

        kwargs.setdefault("temp_audiofile", self._base_dir / "temp_audio.mp3")
        kwargs.setdefault("fps", fps)

        movie.write_videofile(path, **kwargs)

    def add_clip(self, clip: moviepy.editor.VideoClip, position: Position = None):
        if position:
            clip = clip.set_position(position)
        self._clips.append(clip)

    def add_background_color(self, color: str):
        color = hex_to_rgb(color)
        self.add_clip(moviepy.editor.ColorClip(size=self.size, color=color))

    def add_background_image(self, path: pathlib.Path | str):
        if pathlib.Path(path).exists():
            self.add_clip(moviepy.editor.ImageClip(str(path)).resize(self.size))

    def add_text(self, txt: str, size: Size, position: Position, **kwargs):
        clip = moviepy.editor.TextClip(txt=txt, size=size, **kwargs)
        self.add_clip(clip, position)

    def add_webcam(self, size: Size, position: Position):
        path = str(self._base_dir / "video" / "webcams.webm")
        clip = moviepy.editor.VideoFileClip(path).resize(size)
        self.add_clip(clip, position)

    def add_desk_share(self, size: Size, position: Position):
        events = ET.parse(self._base_dir / "deskshare.xml").findall("./event")

        video_url = str(self._base_dir / "deskshare" / "deskshare.webm")
        video = moviepy.editor.VideoFileClip(video_url)

        for event in events:
            t_start = float(event.get("start_timestamp"))
            t_stop = float(event.get("stop_timestamp"))

            clip = video.subclip(t_start, t_stop).resize(size)

            self.add_clip(clip, position)
