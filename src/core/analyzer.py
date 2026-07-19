from pathlib import Path
import re

from src.models.project import Project
from src.models.episode import Episode


class Analyzer:
    """
    项目目录分析器

    负责：
    读取000交付目录
    区分：
        原始交付
        拆集后交付

    输出：
        Project对象
    """


    VIDEO_EXTS = [
        ".mp4",
        ".mov",
        ".mkv"
    ]



    VERSIONS = [
        "00成片",
        "1.有音乐无字幕版本",
        "2.无音乐无字幕无bgm",
        "3.字幕文件"
    ]



    def __init__(self, root_path):

        self.root_path = Path(
            root_path
        )



    def analyze(self):

        project = Project()

        project.root_path = str(
            self.root_path
        )

        project.name = (
            self.root_path.name
        )


        # ======================
        # 扫描原始交付
        # ======================

        for version in self.VERSIONS:

            folder = (
                self.root_path
                /
                version
            )

            if folder.exists():

                self.scan_folder(
                    folder,
                    version,
                    project,
                    split=False
                )



        # ======================
        # 扫描拆集后交付
        # ======================

        split_root = (
            self.root_path
            /
            "拆集后交付"
        )


        if split_root.exists():

            for version in self.VERSIONS:

                folder = (
                    split_root
                    /
                    version
                )


                if folder.exists():

                    self.scan_folder(
                        folder,
                        version,
                        project,
                        split=True
                    )



        self.calculate(
            project
        )


        return project




    def scan_folder(
        self,
        folder,
        version,
        project,
        split=False
    ):


        for file in folder.iterdir():

            if not file.is_file():
                continue


            if file.suffix.lower() not in self.VIDEO_EXTS:

                continue



            result = self.parse_episode(
                file.name
            )


            if not result:

                continue



            ep = Episode(

                original_episode=
                result["episode"],


                part=
                result["part"],


                file_path=
                str(file)

            )



            if split:


                # 保存拆集文件

                project.add_split_video(
                    version,
                    ep
                )


                # 保存拆集关系

                project.add_split_map(
                    ep.original_episode,
                    ep.part
                )



            else:


                # 保存原始文件

                project.add_original(
                    version,
                    ep
                )





    def parse_episode(
        self,
        filename
    ):


        name = Path(
            filename
        ).stem



        # 例如:
        #
        # 03-1

        match = re.match(
            r"(\d+)-(\d+)",
            name
        )


        if match:

            return {

                "episode":
                int(match.group(1)),


                "part":
                int(match.group(2))

            }




        # 例如:
        #
        # 03


        match = re.match(
            r"(\d+)",
            name
        )


        if match:

            return {

                "episode":
                int(match.group(1)),


                "part":
                0

            }



        return None





    def calculate(
        self,
        project
    ):


        # 原始集数

        numbers = []


        for versions in project.original_videos.values():

            for ep in versions:

                numbers.append(
                    ep.original_episode
                )



        if numbers:

            project.original_count = max(
                numbers
            )



        # 最终数量

        split_add = 0


        for old, parts in project.split_map.items():

            split_add += len(parts)



        project.final_count = (

            project.original_count
            -
            len(project.split_map)
            +
            split_add

        )