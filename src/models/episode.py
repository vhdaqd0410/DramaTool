from dataclasses import dataclass
from pathlib import Path


@dataclass
class Episode:
    """
    单集视频/字幕信息
    """

    original_episode: int
    file_path: str

    # 拆集编号
    # 例如:
    # 03.mp4  -> 0
    # 03-1.mp4 -> 1
    # 03-2.mp4 -> 2
    part: int = 0

    # 最终交付编号
    new_episode: int = 0


    @property
    def filename(self):
        return Path(self.file_path).name


    @property
    def extension(self):
        return Path(self.file_path).suffix


    def display_name(self):

        if self.part:

            return (
                f"{self.original_episode:02d}-"
                f"{self.part}"
            )

        return f"{self.original_episode:02d}"


    def __str__(self):

        return (
            f"{self.display_name()} "
            f"({self.filename})"
        )