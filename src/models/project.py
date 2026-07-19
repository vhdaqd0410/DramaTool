from dataclasses import dataclass, field
from typing import Dict, List

from .episode import Episode


@dataclass
class Project:
    """
    短剧交付项目模型

    负责保存：
    1. 原始交付文件
    2. 拆集后文件
    3. 拆集关系
    4. 最终编号映射
    """


    # 项目名称
    name: str = ""


    # 项目根目录
    root_path: str = ""


    # 原始集数
    original_count: int = 0


    # 最终集数
    final_count: int = 0



    # ==========================
    # 原始交付
    #
    # {
    #   "00成片":[Episode...]
    # }
    #
    # ==========================

    original_videos: Dict[
        str,
        List[Episode]
    ] = field(
        default_factory=dict
    )



    # ==========================
    # 拆集后交付
    #
    # {
    #   "00成片":[Episode...]
    # }
    #
    # ==========================

    split_videos: Dict[
        str,
        List[Episode]
    ] = field(
        default_factory=dict
    )



    # ==========================
    # 拆集关系
    #
    # {
    #    3:[1,2],
    #    6:[1,2]
    # }
    #
    # ==========================

    split_map: Dict[
        int,
        List[int]
    ] = field(
        default_factory=dict
    )



    # ==========================
    # 最终编号
    #
    # {
    #    1:"01",
    #    2:"02",
    #    3:"03-1"
    # }
    #
    # ==========================

    episode_mapping: Dict[
        int,
        str
    ] = field(
        default_factory=dict
    )



    # 添加原始文件

    def add_original(
        self,
        version: str,
        episode: Episode
    ):

        if version not in self.original_videos:

            self.original_videos[
                version
            ] = []


        self.original_videos[
            version
        ].append(
            episode
        )



    # 添加拆集文件

    def add_split_video(
        self,
        version: str,
        episode: Episode
    ):

        if version not in self.split_videos:

            self.split_videos[
                version
            ] = []


        self.split_videos[
            version
        ].append(
            episode
        )



    # 添加拆集关系

    def add_split_map(
        self,
        original_episode: int,
        part: int
    ):

        if original_episode not in self.split_map:

            self.split_map[
                original_episode
            ] = []


        if part not in self.split_map[
            original_episode
        ]:

            self.split_map[
                original_episode
            ].append(
                part
            )



    # 获取某版本全部文件

    def get_version_files(
        self,
        version
    ):

        result = []


        if version in self.original_videos:

            result.extend(
                self.original_videos[
                    version
                ]
            )


        if version in self.split_videos:

            result.extend(
                self.split_videos[
                    version
                ]
            )


        return result



    # 项目统计

    def summary(self):

        return {

            "项目":
            self.name,


            "原始集数":
            self.original_count,


            "最终集数":
            self.final_count,


            "拆集数量":
            len(self.split_map),


            "原始版本数量":
            len(
                self.original_videos
            ),


            "拆集版本数量":
            len(
                self.split_videos
            )

        }



    def __str__(self):

        return (
            f"{self.name}\n"
            f"原始:{self.original_count}\n"
            f"最终:{self.final_count}\n"
            f"拆集:{len(self.split_map)}"
        )