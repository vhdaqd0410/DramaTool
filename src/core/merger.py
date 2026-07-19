import os
import shutil



class Merger:
    """
    DramaTool 文件整理模块

    功能:

    读取:
        Project

    根据:
        episode_mapping

    生成:

        项目名_拆集版

            ├──00成片
            ├──1.有音乐无字幕版本
            ├──2.无音乐无字幕无bgm
            └──3.字幕文件

    """


    VERSIONS = [

        "00成片",

        "1.有音乐无字幕版本",

        "2.无音乐无字幕无bgm",

        "3.字幕文件"

    ]



    def __init__(self):

        pass



    def merge(self, project):

        """
        开始整理
        """


        root_path = project.root_path


        if not root_path:

            raise Exception(
                "项目路径为空"
            )



        output_path = (

            root_path.rstrip("\\/")

            +

            "_拆集版"

        )



        print(
            "输出目录:",
            output_path
        )



        self.create_dirs(
            output_path
        )



        for version in self.VERSIONS:


            print(
                "正在处理:",
                version
            )



            self.merge_version(

                project,

                version,

                output_path

            )



        print(
            "整理完成"
        )


        return output_path





    def create_dirs(
            self,
            output_path
    ):


        for version in self.VERSIONS:


            folder = os.path.join(

                output_path,

                version

            )


            os.makedirs(

                folder,

                exist_ok=True

            )





    def merge_version(

            self,

            project,

            version,

            output_path

    ):


        files = self.collect_files(

            project,

            version

        )



        target_dir = os.path.join(

            output_path,

            version

        )



        for final_index, source_name in project.episode_mapping.items():


            source_file = files.get(

                source_name

            )


            if not source_file:


                print(

                    "缺少文件:",

                    source_name

                )

                continue



            ext = os.path.splitext(

                source_file

            )[1]



            target_name = (

                f"{final_index:02d}{ext}"

            )



            target_file = os.path.join(

                target_dir,

                target_name

            )



            shutil.copy2(

                source_file,

                target_file

            )



            print(

                "复制:",

                source_name,

                "→",

                target_name

            )






    def collect_files(

            self,

            project,

            version

    ):

        """
        收集某个版本所有文件

        返回:

        {
            "01":路径,
            "03-1":路径
        }

        """


        result = {}



        # =====================
        # 原始文件
        # =====================

        if version in project.original_videos:


            for item in project.original_videos[version]:


                result[

                    item.display_name()

                ] = item.file_path





        # =====================
        # 拆集文件
        # =====================

        if version in project.split_videos:


            for item in project.split_videos[version]:


                result[

                    item.display_name()

                ] = item.file_path





        return result