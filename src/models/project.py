from dataclasses import dataclass, field
from typing import List, Dict

from .episode import Episode


@dataclass
class Project:
    """
    短剧项目数据模型
    """

    # 项目名称
    name: str = ""

    # 项目路径
    root_path: str = ""

    # 原始集数
    original_count: int = 0

    # 最终集数
    final_count: int = 0


    # 四个交付版本
    videos: Dict[str, List[Episode]] = field(
        default_factory=dict
    )


    # 拆集关系
    #
    # 示例:
    #
    # {
    #   3:[1,2],
    #   6:[1,2]
    # }
    #
    split_map: Dict[int, List[int]] = field(
        default_factory=dict
    )


    # 最终编号映射
    #
    # 示例:
    #
    # {
    #   1:"01",
    #   2:"02",
    #   3:"03-1"
    # }
    #
    episode_mapping: Dict[int, str] = field(
        default_factory=dict
    )


    def add_episode(
        self,
        version: str,
        episode: Episode
    ):

        if version not in self.videos:
            self.videos[version] = []

        self.videos[version].append(
            episode
        )


    def add_split(
        self,
        original_episode: int,
        parts: List[int]
    ):

        self.split_map[
            original_episode
        ] = parts


    def summary(self):

        return {

            "项目": self.name,

            "原始集数":
                self.original_count,

            "最终集数":
                self.final_count,

            "拆集数量":
                len(self.split_map),

            "版本数量":
                len(self.videos)

        }


    def __str__(self):

        return (
            f"{self.name}\n"
            f"原始:{self.original_count}\n"
            f"最终:{self.final_count}"
        )